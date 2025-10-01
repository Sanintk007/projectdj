from django import template

register= template.Library()

@register.simple_tag(name='getgrandtotal')
def getgrandtotal(cart, rate=0.18):
    """Calculate total price including tax."""
    subtotal = sum(item.product.price * item.quantity for item in cart.added_items.all() if item.product)
    tax = subtotal * rate
    return round(subtotal + tax, 2)