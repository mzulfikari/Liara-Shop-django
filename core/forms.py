from django import forms
from .models import ContactUs


class ContactUs(forms.ModelForm):
    model = ContactUs
    fields = "__all__"
