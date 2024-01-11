from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

from races.views import ManagerContextMixin

class DriverMarketView(LoginRequiredMixin, View):
    template_name = "market/market.html"

    def get(self, request):
        return render(request, self.template_name)
    

