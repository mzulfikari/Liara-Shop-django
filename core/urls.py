from django.urls import path
from . import views

# نام اپ کاربران
app_name = "Core"

urlpatterns = [
    path("aboute", views.About_Me.as_view(), name="About_me"),
    path("contact", views.Contact_Us.as_view(), name="Contact_us"),
]
