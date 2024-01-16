from django.test import TestCase

from messaging.forms import NewMessageForm
from messaging.helpers import send_message
from messaging.models import Message
from manager.models import Manager, User


class MessageModelTestCase(TestCase):
    
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
        recipient = Manager.objects.create(
            name="recipient",
            user=User.objects.create(
                username="recipient_user",
                password="123",
                email="recipient.email@test.com",
            ),
        )

        self.message = Message.objects.create(
            sender=sender,
            recipient=recipient,
            subject="test subject",
            content="test content 123 456",
        )

    def test_read_method(self):
        # Initial state is not read
        self.assertFalse(self.message.read)

        # Set read and test
        self.message.set_read(self.message.recipient)
        updated_message = Message.objects.get(id=self.message.id)
        self.assertTrue(updated_message.read)

    def test_read_method_wrong_manager(self):
        # Initial state is not read
        self.assertFalse(self.message.read)

        # Set read with wrong manager and test
        self.message.set_read(self.message.sender)
        updated_message = Message.objects.get(id=self.message.id)
        self.assertFalse(updated_message.read)

    def test_delete_message_method(self):
        # Message exists
        self.assertTrue(Message.objects.filter(id=self.message.id).exists())

        # Delete and test
        self.message.delete_message(self.message.recipient)
        self.assertFalse(Message.objects.filter(id=self.message.id).exists())

    def test_delete_message_method_wrong_manager(self):
        # Message exists
        self.assertTrue(Message.objects.filter(id=self.message.id).exists())

        # Try to delete but failed and test
        self.message.delete_message(self.message.sender)
        self.assertTrue(Message.objects.filter(id=self.message.id).exists())

    def test_reply_valid_form(self):
        form_data = {
            "recipient": self.message.sender,
            "subject": f"Re: {self.message.subject}",
            "content": "Test reply content 123 456",
        }
        reply_form = NewMessageForm(data=form_data)
        self.assertTrue(reply_form.is_valid())

        # Reply to message and check if message created
        self.message.reply(reply_form)
        reply_messages = Message.objects.filter(sender=self.message.recipient, recipient=self.message.sender)
        self.assertEqual(reply_messages.count(), 1)

    def test_reply_invalid_form(self):
        form_data = {
            "recipient": "",
            "subject": f"Re: {self.message.subject}",
            "content": "Test reply content 123 456",
        }
        reply_form = NewMessageForm(data=form_data)
        self.assertFalse(reply_form.is_valid())

    def test_reply_to_yourself(self):
        form_data = {
            "recipient": self.message.sender,
            "subject": f"Re: {self.message.subject}",
            "content": "Test reply content 123 456",
        }
        reply_form = NewMessageForm(data=form_data)
        self.assertTrue(reply_form.is_valid())
        self.message.reply(reply_form)
        reply_messages = Message.objects.filter(sender=self.message.recipient, recipient=self.message.recipient)
        self.assertEqual(reply_messages.count(), 0)
        

class SendMessageTestCase(TestCase):

    def setUp(self):
        # Create mock manager, message
        self.sender = Manager.objects.create(
            name="sender",
            user=User.objects.create(
                username="sender_user", 
                password="123", 
                email="sender.email@test.com",
                ),        
        )
        self.recipient = Manager.objects.create(
            name="recipient",
            user=User.objects.create(
                username="recipient_user",
                password="123",
                email="recipient.email@test.com",
            ),
        )
        form_data = {
            "recipient": self.recipient,
            "subject": "Test",
            "content": "Test reply content 123 456",
        }
        self.send_message_form = NewMessageForm(data=form_data)

    def test_send_message(self):
        # Check if form is valid and message created
        self.assertTrue(self.send_message_form.is_valid())
        send_message(self.sender, self.send_message_form)
        self.assertTrue(Message.objects.filter(sender=self.sender, recipient=self.recipient).exists())