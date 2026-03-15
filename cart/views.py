from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_cart(request):
    """
    Display the shopping cart contents
    """
    cart = request.session.get('cart', {})
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

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'cart/cart.html', context)


def add_to_cart(request, item_id):
    """
    Add a quantity of the specified product to the shopping cart
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})

    item_id = str(item_id)

    if item_id in cart:
        cart[item_id] += quantity
        messages.success(request, f'Updated {product.name} quantity in your cart.')
    else:
        cart[item_id] = quantity
        messages.success(request, f'Added {product.name} to your cart.')

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('view_cart')


def update_cart(request, item_id):
    """
    Update the quantity of the specified product in the shopping cart
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})

    item_id = str(item_id)

    if quantity > 0:
        cart[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity.')
    else:
        cart.pop(item_id, None)
        messages.success(request, f'Removed {product.name} from your cart.')

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('view_cart')


def remove_from_cart(request, item_id):
    """
    Remove the specified product from the shopping cart
    """
    product = get_object_or_404(Product, pk=item_id)
    cart = request.session.get('cart', {})

    item_id = str(item_id)

    cart.pop(item_id, None)
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f'Removed {product.name} from your cart.')

    return redirect('view_cart')
