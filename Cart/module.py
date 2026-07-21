from Products.models import Products
from django.contrib.sessions.backends.db import SessionStore

CART_SESSION_ID = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session["CART_SESSION_ID"] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            item["product"] = Products.objects.get(id=int(item["id"]))
            item["total"] = int(item["quantity"]) * int(item["price"])
            yield item

    def unique_id_generator(self, id, color, size):
        result = f"{id}-{color}-{size}"
        return result

    def add(self, product, value, color, size):
        unique = self.unique_id_generator(product.id, color, size)
        if unique not in self.cart:
            self.cart[unique] = {
                "value": 0,
                "price": str(product.price),
                "color": color,
                "size": size,
                "id": product.id,
            }
        self.cart[unique]["value"] += int(value)
        self.save()

    def save(self):
        self.session.modifild = True
