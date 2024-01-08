from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View, DetailView
from django.views.generic.base import ContextMixin
from django.urls import reverse

from messaging.models import Message
from messaging.forms import NewMessageForm, DeleteMessageForm
from manager.models import Manager


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
        context['sent_messages'] = Message.objects.filter(sender=context["current_user_manager"])
        context['received_messages'] = Message.objects.filter(receiver=context["current_user_manager"])
        return context
    

class MessageView(LoginRequiredMixin, ManagerContextMixin, DetailView):
    model = Message
    template_name = "messaging/message.html"
    context_object_name = "message"

    def get_object(self, queryset=None):
        message = Message.objects.get(pk=self.kwargs['id'])
        return message
    
    def get(self, request, id):
        response = super().get(request, id)
        self.object.set_read(Manager.objects.get(user=request.user))
        form = DeleteMessageForm(id)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        if "delete_message_id" in request.POST:
            form = DeleteMessageForm(id, request.POST)
            if form.is_valid():
                message = Message.objects.get(id=form.cleaned_data["delete_message_id"])
                message.delete_message(Manager.objects.get(user=request.user))
            else:
                return HttpResponseRedirect(reverse("manager:index"))
        return HttpResponseRedirect(reverse("messaging:messages_overview"))


class NewMessageView(LoginRequiredMixin, ManagerContextMixin, TemplateView):
    template_name = "messaging/new_message.html"
    
    def get(self, request, receiver_id=None):
        form = NewMessageForm()
        context = self.get_context_data()
        context['form'] = form

        if receiver_id is not None:
            # Logic if receiver is known
            receiver = Manager.objects.get(id=receiver_id)
            context['receiver'] = receiver
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = NewMessageForm(request.POST)
        if form.is_valid():
            sender = Manager.objects.get(user=request.user)
            receiver = Manager.objects.get(id=form.cleaned_data["receiver_id"])
            subject = form.cleaned_data["subject"]
            content = form.cleaned_data["content"]
            message = Message(
                sender=sender,
                receiver=receiver,
                subject=subject,
                content=content,
            )
            message.save()
            return HttpResponseRedirect(reverse("messaging:messages_overview"))
        else:
            context = self.get_context(form)
            return render(request, self.template_name, context)
        
    def get_context(self, form):
        context = self.get_context_data()
        context.update({
            "form": form,
        })
        return context



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
