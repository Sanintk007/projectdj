from django import template

register= template.Library()

@register.simple_tag(name='getsubtotal')
def getsubtotal(cart):
    total=0
    for item in cart.added_items.all():
        total+=item.quantity*item.product.price
    return total    