from django.core.mail import send_mail


def send_welcome_email(self, email):
        subject = 'Welcome to Circuitrix!'
        message = 'Greetings! You have successfully registered on our portal. Good luck!'
        from_email = 'settings.EMAIL_HOST_USER'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)