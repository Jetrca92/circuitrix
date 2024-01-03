from django.urls import path

from messaging.views import MessagesInboxView, NewMessageView

app_name = "messaging"

urlpatterns = [
    path("messages", MessagesInboxView.as_view(), name="messages_overview"),
    path("new-message", NewMessageView.as_view(), name="new_message"),
]
