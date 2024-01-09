from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View, DetailView
from django.views.generic.base import ContextMixin
from django.urls import reverse

from messaging.models import Message
from messaging.helpers import send_message
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
        form_reply = NewMessageForm()
        context = self.get_context_data()
        context['form'] = form
        context['form_reply'] = form_reply
        context['receiver'] = self.object.sender
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        # Handle message deletion
        if "delete_message_id" in request.POST:
            form = DeleteMessageForm(id, request.POST)
            if form.is_valid():
                message = Message.objects.get(id=form.cleaned_data["delete_message_id"])
                message.delete_message(Manager.objects.get(user=request.user))
        # Handle message reply
        if "receiver_id" in request.POST:
            form = NewMessageForm(request.POST)
            if form.is_valid():
                message = self.get_object()
                message.reply(form)
                return HttpResponseRedirect(reverse("messaging:messages_overview"))
            else:
                context = self.get_context(form)
                return render(request, self.template_name, context)
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
            send_message(Manager.objects.get(user=request.user), form)
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
