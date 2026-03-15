from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .forms import OrderForm
from .models import Order, OrderItem


def checkout(request):
    """
    Display the checkout page and handle order submission
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

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.order_total = total
            order.save()

            for item_id, quantity in cart.items():
                product = get_object_or_404(Product, pk=item_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                )

            request.session['cart'] = {}
            messages.success(request, "Order placed successfully!")
            return redirect('checkout_success', order_id=order.id)

    else:
        form = OrderForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_id):
    """
    Display successful checkout confirmation
    """
    order = get_object_or_404(Order, pk=order_id)

    return render(request, 'checkout/checkout_success.html', {
        'order': order,
    })