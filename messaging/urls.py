from django.urls import path

from messaging.views import MessagesInboxView, NewMessageView, MessageView

app_name = "messaging"

urlpatterns = [
    path("messages", MessagesInboxView.as_view(), name="messages_overview"),
    path("new-message", NewMessageView.as_view(), name="new_message"),
    path("new-message/<int:receiver_id>/", NewMessageView.as_view(), name="new_message_with_user"),
    path("message/<int:id>", MessageView.as_view(), name="message"),
]
