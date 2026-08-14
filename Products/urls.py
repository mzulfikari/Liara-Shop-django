from django.urls import path, re_path
from . import views

app_name = "Product"

urlpatterns = [
    re_path( r"products/(?P<slug>[-\w]+)/details", views.ProductDetails.as_view(),name="Product_details",),
    path("", views.Product_View.as_view(), name="Product_view"),
    path("product/list", views.Product_list.as_view(), name="Product_list"),
    path("favorites/toggle/<int:product_id>/",views.ToggleFavoriteView.as_view(),name="toggle-favorite")
]
