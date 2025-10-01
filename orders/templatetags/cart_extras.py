# first we created seperate tags for subtotal(getsubtotal.py),tax(gettax.py),total(gettotal) instead of making it complicated we create a single tag name cart_extras.py and included everything in it and loaded in the cart_container.html . for reference im keeping old tag as it is

from django import template

register = template.Library()

@register.simple_tag
def getsubtotal(cart):
    """Return subtotal (sum of all items * qty)."""
    if not cart:
        return 0
    return sum(
        item.product.price * item.quantity
        for item in cart.added_items.all()
        if item.product
    )

@register.simple_tag
def gettax(cart):
    """Return tax (example: 18% of subtotal)."""
    subtotal = getsubtotal(cart)
    return round(subtotal * 0.18, 2)   # Change 0.18 → your tax %

@register.simple_tag
def gettotal(cart):
    """Return grand total (subtotal + tax)."""
    subtotal = getsubtotal(cart)
    tax = gettax(cart)
    return subtotal + tax
