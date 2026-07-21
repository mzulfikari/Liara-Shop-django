from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from Products.models import Products
from .module import Cart


class CartDetail(View):
    def get(self, request):
        cart = Cart(request)
        print(cart)
        context = {"cart": cart}
        return render(request, "cart/cart.html", context)


class CartIncludeProduct(View):
    def get(self, request):
        cart = Cart(request)
        print(cart)
        context = {"cart": cart}
        return render(request, "cart/include/includ_cart.html", context)


class CartAdd(View):

    def post(self, request, pk):
        product = get_object_or_404(Products, id=pk)
        color, size, value = (request.POST.get("color", ""),)
        request.POST.get("size"),
        request.POST.get("value")

        cart = Cart(request)
        cart.add(product, color, size, value)

        messages.success(request, "محصول به سبد خرید اضافه شد!")

        return redirect("cart/cart.html")
