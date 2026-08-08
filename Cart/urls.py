from django.urls import path
from . import views

app_name = "Cart"

urlpatterns = [
    path("session/add-product/", views.SessionAddProductView.as_view(),name="session-add-product"),
    path("cart/detail", views.CartSummaryView.as_view(),name="cart-detail"),
    path('session/remove/product/',views.SessionRemoveProductView.as_view(),name="session-remove-product"),
    path('session/update/product/',views.SessionUpdateProductQuantityView.as_view(),name="session-update-product"),
]
