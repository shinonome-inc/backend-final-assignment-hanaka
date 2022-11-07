# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView


# Create your views here.
class HomeView(TemplateView):
    template_name = "tweets/home.html"
    success_url = reverse_lazy("home")
