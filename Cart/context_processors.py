from .cart import CartSession

def cart_processors(request):
      cart = CartSession(request.session)
      return {"cart":cart}