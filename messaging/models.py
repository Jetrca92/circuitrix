from django.db import models
from manager.models import Manager


class Message(models.Model):
    sender = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='sent')
    recipient = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='received')
    subject = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} to {self.recipient} - {self.timestamp}'
    
    def set_read(self, manager):
        # Only set read=True if recipient opens
        if self.recipient == manager:
            self.read = True
            self.save()

    def delete_message(self, manager):
        if self.recipient == manager:
            self.delete()

    def reply(self, form):
        # Can't reply to yourself
        if self.recipient == form.cleaned_data["recipient"]:
            return
        
        message = Message(
            sender=self.recipient,
            recipient=form.cleaned_data["recipient"],
            subject=form.cleaned_data["subject"],
            content=form.cleaned_data["content"],
        )
        message.save()
