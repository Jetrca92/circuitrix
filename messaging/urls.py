from django.urls import path

from messaging.views import MessagesInboxView, NewMessageView

app_name = "messaging"

urlpatterns = [
    path("mail", MessagesInboxView.as_view(), name="messages_overview"),
    path("new-mail", NewMessageView.as_view(), name="new_message"),
]
