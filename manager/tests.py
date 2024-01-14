from django.test import TestCase

from manager.models import User, Manager
from messaging.models import Message


class UnreadMessagesTest(TestCase):
    
    def setUp(self):
        # Create mock manager, message
        sender = Manager.objects.create(
            name="sender",
            user=User.objects.create(
                username="sender_user", 
                password="123", 
                email="sender.email@test.com",
                ),        
        )
        receiver = Manager.objects.create(
            name="receiver",
            user=User.objects.create(
                username="receiver_user",
                password="123",
                email="receiver.email@test.com",
            ),
        )

        self.message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            subject="test subject",
            content="test content 123 456",
        )

    def test_unread_message_method(self):
        # Sender has no new received messages
        self.assertFalse(self.message.sender.unread_messages())

        # Receiver has new unread messages
        self.assertTrue(self.message.receiver.unread_messages())
        