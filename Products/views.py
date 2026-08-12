from django.contrib import messages
from urllib import request
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from Products.models import Products, Comment, Color, ProductStatusType, Category
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import FieldError
from django.utils.encoding import uri_to_iri
from django.shortcuts import get_object_or_404

class ProductDetails(DetailView):
    template_name = "Product/single-product.html"
    model = Products
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["colors"] = product.color.all()
        context["related_products"] = Products.objects.filter(
            category=product.category, status=ProductStatusType.publish.value
        ).exclude(pk=product.pk)[:8]
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
    def get_object(self, **kwargs):
        slug = self.kwargs.get("slug")

        print("========== PRODUCT DEBUG ==========")
        print("RAW SLUG:", repr(slug))
        print("DECODED SLUG:", repr(uri_to_iri(slug)))

        product = get_object_or_404(
            Products,
            slug=uri_to_iri(slug)
        )

        print("PRODUCT:", product)
        print("DB SLUG:", repr(product.slug))
        print("===================================")

        return product

class Product_View(ListView):
    model = Products
    template_name = "Product/index.html"
    context_object_name = "Products"
    queryset = Products.objects.filter(status=ProductStatusType.publish.value)
    paginate_by = 8

    def get_queryset(self):
        queryset = Products.objects.filter(status=ProductStatusType.publish.value)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

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
