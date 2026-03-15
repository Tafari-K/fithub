from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .forms import OrderForm


def checkout(request):
    """
    Display the checkout page with order form and cart summary
    """
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('product_list')

    cart_items = []
    total = 0

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    form = OrderForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'checkout/checkout.html', context)
