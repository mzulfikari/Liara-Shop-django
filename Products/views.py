from django.contrib import messages
from urllib import request
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from Products.models import Products, Comment, Color, ProductStatusType, Category
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect


class ProductDetails(DetailView):
    template_name = "Product/single-product.html"
    model = Products
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["colors"] = product.color.all()
        return context

    def post(self, request, pk):

        if request.user.is_authenticated:
            self.object = self.get_object()
            parent_id = request.POST.get("parent_id")
            body = request.POST.get("body")

            if body:
                Comment.objects.create(
                    body=body,
                    products=self.object,
                    user=request.user,
                    parent_id=parent_id,
                )
            else:
                messages.error(request, "متن نظر نمی‌تواند خالی باشد.")
            return redirect(request.path)


class Product_View(ListView):
    model = Products
    template_name = "Product/index.html"
    context_object_name = "Products"
    queryset = Products.objects.filter(status=ProductStatusType.publish.value)
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["discount_products"] = Products.objects.filter(
            status=ProductStatusType.publish.value, Discounts=True
        )
        return context


class Product_list(ListView):
    model = Products
    template_name = "Product/list_view.html"
    paginate_by = 2

    def get_queryset(self):
        queryset = Products.objects.filter(status=ProductStatusType.publish.value)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.getlist("category_id"):
            queryset = queryset.filter(category__id__in=category_id).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["selected_categories"] = self.request.GET.getlist("category_id")
        return context
