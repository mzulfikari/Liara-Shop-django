from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def rial_price(value):
    try:
        value = int(value)
        formatted = f"{value:,}"
        return f"{formatted} تومان"
    except (ValueError, TypeError):
        return value
