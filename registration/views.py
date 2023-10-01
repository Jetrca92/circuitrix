from .forms import RegistrationForm
from manager.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('manager:index')


