from django.db import models
from manager.models import Manager


class Message(models.Model):
    sender = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='sent')
    receiver = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='received')
    subject = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} to {self.receiver} - {self.timestamp}'
    
    def set_read(self, manager):
        # Only set read=True if receiver opens
        if self.sender != manager:
            self.is_read = True
            self.save()

    def delete_message(self, manager):
        if self.receiver == manager:
            self.delete()
