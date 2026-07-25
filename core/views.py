from django.shortcuts import render, redirect
from .forms import ContactUsForm
from Products.models import Products
from django.db import models
from .models import *
from django.views.generic import TemplateView,DetailView,CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

class About_Me(TemplateView):    
    template_name = "contact-us/aboute-me.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["about"] = AboutMe.objects.first()
        return context

class ContactUsView(CreateView,SuccessMessageMixin):
    template_name = "contact-us/contact-us.html"
    form_class = ContactUsForm
    model = ContactUs
    success_message = "تیکت شما ثبت شد.پس از بررسی تماس خواهیم گرفت"
    success_url = reverse_lazy("Core:Contact_us")
    

class Welcome(TemplateView):
    template_name = "welcome.html"
