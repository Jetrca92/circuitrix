from django.urls import path

from messaging.views import MailInboxView, NewMailView

app_name = "messaging"

urlpatterns = [
    path("mail", MailInboxView.as_view(), name="mail_overview"),
    path("new-mail", NewMailView.as_view(), name="new_mail"),
]
