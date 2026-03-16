import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .forms import OrderForm
from .models import Order, OrderItem
from profiles.models import UserProfile

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
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

    amount = int(total * 100)

    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='gbp',
        automatic_payment_methods={'enabled': True},
    )

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.order_total = total
            order.stripe_pid = intent.id
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
        try:
            profile = UserProfile.objects.get(user=request.user)

            form = OrderForm(initial={
                'full_name': request.user.username,
                'email': request.user.email,
                'phone_number': profile.default_phone_number,
                'street_address1': profile.default_street_address1,
                'street_address2': profile.default_street_address2,
                'town_or_city': profile.default_town_or_city,
                'postcode': profile.default_postcode,
                'country': profile.default_country,
            })

        except UserProfile.DoesNotExist:
            form = OrderForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'total': total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request):

    return render(request, 'checkout/checkout_success.html')
