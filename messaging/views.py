from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View, DetailView
from django.views.generic.base import ContextMixin

from messaging.models import Message
from messaging.forms import NewMessageForm
from manager.models import Team


class ManagerContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manager = self.request.user.manager
        context['current_user_manager'] = manager
        return context
    

class MessagesInboxView(LoginRequiredMixin, ManagerContextMixin, TemplateView):
    model = Message
    template_name="messaging/messages_overview.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['sent_messages'] = Message.objects.filter(sender=user)
        context['received_messages'] = Message.objects.filter(receiver=user)
        return context
    

class MessageView(LoginRequiredMixin, ManagerContextMixin, DetailView):
    model = Message
    template_name = "messages/message.html"
    context_object_name = "message"

    def get_object(self, queryset=None):
        message = Message.objects.get(pk=self.kwargs['id']  )
        return message
    

class NewMessageView(LoginRequiredMixin, ManagerContextMixin, TemplateView):
    template_name = "messaging/new_message.html"
    
    def get(self, request, receiver_id=None):
        form = NewMessageForm()
        context = self.get_context_data()
        context['form'] = form

        if receiver_id is not None:
            # Logic if receiver is known
            pass
        return render(request, self.template_name, context)
    
    def post(self, request):
        pass


"""
@transaction.atomic
@login_required
def letter(request, mail_id):
    resident = Resident.objects.get(resident_user=request.user)
    letter = Mail.objects.get(id=mail_id)
    letter.set_read(resident)
    # Display letter via get
    if request.method != "POST":    
        return render(request, "game/letter.html", {
            "resident": resident,
            "letter": letter,
        })
    
    # Form for letter delete sent
    if "delete_letter_id" in request.POST:
        letter.delete()
        return HttpResponseRedirect(reverse("mail"))
    
    # Form for reply letter sent
    if "topic_reply" in request.POST:
        letter.reply(request.POST["topic_reply"], request.POST["message_reply"])
        return HttpResponseRedirect(reverse("mail"))
    

@transaction.atomic
@login_required
def new_letter(request, recipient_id):
    resident = Resident.objects.get(resident_user=request.user)
    recipient = Resident.objects.get(id=recipient_id)
    # Display new_letter.html via get
    if request.method != "POST":
        return render(request, "game/new_letter.html", {
            "resident": resident,
            "user_profile": recipient,
        })
    
    # Letter was sent
    letter = Mail(
        recipient=recipient, 
        sender=resident, 
        topic=request.POST["topic"], 
        message=request.POST["message"], 
    )
    letter.save()
    return HttpResponseRedirect(reverse("mail"))
    """
