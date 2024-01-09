from manager.models import Manager
from messaging.models import Message


def send_message(sender, form):
    message = Message(
        sender=sender,
        receiver=Manager.objects.get(id=form.cleaned_data["receiver_id"]),
        subject=form.cleaned_data["subject"],
        content=form.cleaned_data["content"],
    )
    message.save()