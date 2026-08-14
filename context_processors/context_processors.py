from Products.models import Category, Products, Brand
from django.db.models import Prefetch
from core.models import SiteSettings, Banner
from django.views.generic import View, TemplateView
from Cart.cart import CartSession
from django.core.cache import cache
from django.conf import settings


def Categories(request):
    cache_key = "site_categories"
    categories = cache.get(cache_key)
    if categories is None:
        categories = list( Category.objects.filter( views=True,products__isnull=False ).distinct() )
        cache.set( cache_key, categories,settings.CACHE_TIMEOUT)
    return { "Categories": categories }


def site_settings(request):
    """Default site settings"""
    try:
        settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        settings = None
    return {"site_settings": settings}


def Banners(request):
    return {
        "header_banners": Banner.objects.filter(
            status="published", pformance_Venue="Header"
        ),
        "discount_banner": Banner.objects.filter(
            status="published", pformance_Venue="Banner for Heavily Discounted Products"
        ).first(),
        "banner_1": Banner.objects.filter(
            status="published", pformance_Venue="Banner 1.1"
        ).first(),
        "banner_2": Banner.objects.filter(
            status="published", pformance_Venue="Banner 1.2"
        ).first(),
        "banner_3": Banner.objects.filter(
            status="published", pformance_Venue="Banner 1.3"
        ).first(),
        "banner_4": Banner.objects.filter(
            status="published", pformance_Venue="Banner 1.4"
        ).first(),
        "banner_2_1": Banner.objects.filter(
            status="published", pformance_Venue="Banner 2.1"
        ).first(),
        "banner_2_2": Banner.objects.filter(
            status="published", pformance_Venue="Banner 2.2"
        ).first(),
    }


def brands(request):
    return {"brands": Brand.objects.all()}


def cart(request):
    cart = CartSession(request.session)
    return {
        "cart_items": cart.get_cart_items(),
        "cart_total_quantity": cart.get_total_quantity(),
        "cart_total_payment": cart.get_total_payment_amount(),
    }
