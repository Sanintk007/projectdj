from django import template

register= template.Library()

@register.simple_tag(name='gettax')
def gettax(cart, rate=0.18):
    """
    Calculate tax for the cart.
    Default = 18% (0.18). 
    You can change rate as needed.
    """
    subtotal = sum(item.product.price * item.quantity for item in cart.added_items.all() if item.product)
    return round(subtotal * rate, 2)

