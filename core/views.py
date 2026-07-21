from django.shortcuts import render, redirect
from .forms import ContactUs
from Products.models import Products
from django.db import models
from django.views.generic import TemplateView

# def contact(request):
#     if request.method == 'POST':
#         form = ContactUs(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('core:home')
#     else:
#         form = ContactUs()

#     context = {
#         'form': form
#     }
#     return render(request, 'core/contact.html', context)


class About_Me(TemplateView):

    template_name = "contact-us/aboute-me.html"


class Contact_Us(TemplateView):

    template_name = "contact-us/contact-us.html"


class Welcome(TemplateView):
    template_name = "welcome.html"
