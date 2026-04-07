import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .forms import OrderForm
from .models import Order, OrderItem, Subscription
from profiles.models import UserProfile
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
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
            messages.success(request, "Your order was placed successfully.")
            return redirect('checkout_success', order_id=order.id)

        else:
            messages.error(request, "There was a problem with your checkout form.")

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


@login_required
def checkout_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'checkout/checkout_success.html', {'order': order})


# ===============================
# STRIPE WEBHOOK HANDLER
# ===============================

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WH_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle event types
    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        handle_payment_intent_succeeded(intent)

    elif event['type'] == 'payment_intent.payment_failed':
        intent = event['data']['object']
        handle_payment_failed(intent)

    return HttpResponse(status=200)


def handle_payment_intent_succeeded(intent):
    stripe_pid = intent.id

    try:
        order = Order.objects.get(stripe_pid=stripe_pid)
        order.paid = True  # make sure this field exists
        order.save()
    except Order.DoesNotExist:
        pass


def handle_payment_failed(intent):
    stripe_pid = intent.id

    try:
        order = Order.objects.get(stripe_pid=stripe_pid)
        order.paid = False
        order.save()
    except Order.DoesNotExist:
        pass


# ===============================
# MEMBERSHIP / SUBSCRIPTIONS
# ===============================

def membership_pricing(request):
    return render(request, 'checkout/membership_pricing.html')


@login_required
def create_subscription_checkout(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("membership_pricing"))

    session = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        customer_email=request.user.email,
        line_items=[{
            "price": settings.STRIPE_PRICE_ID,
            "quantity": 1,
        }],
        metadata={
            "user_id": str(request.user.id),
            "username": request.user.username,
        },
        success_url=request.build_absolute_uri(
            reverse("subscription_success")
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(
            reverse("membership_pricing")
        ),
    )

    return HttpResponseRedirect(session.url)


def subscription_success(request):
    return render(request, "checkout/subscription_success.html")


@login_required
def premium_plans(request):
    try:
        subscription = request.user.subscription
    except Subscription.DoesNotExist:
        messages.error(request, "You need an active membership.")
        return redirect('membership_pricing')

    if not subscription.membership_active:
        messages.error(request, "You need an active membership.")
        return redirect('membership_pricing')

    return render(request, 'checkout/premium_plans.html')