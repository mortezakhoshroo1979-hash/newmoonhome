from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout.html'
