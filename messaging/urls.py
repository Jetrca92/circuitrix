from django.urls import path

from messaging.views import MailInboxView

app_name = "messaging"

urlpatterns = [
    path("mail", MailInboxView.as_view(), name="mail_overview"),
    
]
