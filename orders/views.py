from django.shortcuts import render, redirect
from .models import Order, OrderedItem
from django.contrib import messages
from products.models import Product
from django.contrib.auth.decorators import login_required

def show_cart(request):
    user = request.user
    customer = user.customer_profile
    print("user",user)
    print("customer",customer)
    cart_obj, created = Order.objects.get_or_create(
        owner=customer,
        order_status=Order.CART_STAGE
    )
    context = {'cart': cart_obj}
    return render(request, 'cart.html', context)



def remove_item_from_cart(request, pk):
    try:
        item = OrderedItem.objects.get(pk=pk)
        item.delete()
    except OrderedItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")
    return redirect('cart')    




@login_required(login_url='account')
def show_orders(request):
    user = request.user
    customer = user.customer_profile
    all_orders=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context={'orders':all_orders}
    return render(request, 'orders.html',context)
    



@login_required(login_url='account')
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        customer = user.customer_profile
        quantity = float(request.POST.get('quantity', 1))
        product_id = request.POST.get('product_id')

        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )

        product = Product.objects.get(pk=product_id)
        ordered_item, created = OrderedItem.objects.get_or_create(
            product=product,
            owner=cart_obj,
        )

        if created:
            ordered_item.quantity = quantity
        else:
            ordered_item.quantity += quantity
        ordered_item.save()

    return redirect('cart')




def checkout_cart(request):
    if request.method == 'POST':
        user = request.user
        customer = user.customer_profile

        # Get the current cart
        order_obj = Order.objects.filter(
            owner=customer,
            order_status=Order.CART_STAGE
        ).first()

        if order_obj and order_obj.added_items.exists():
            # Confirm the order
            order_obj.order_status = Order.ORDER_CONFIRMED
            order_obj.save()
            messages.success(
                request,
                'Your order is processed. Your items will be delivered within a few days.'
            )
        else:
            messages.error(request, 'Unable to process. No item in cart.')

    return redirect('cart')
