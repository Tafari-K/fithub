def cart_contents(request):
    """
    Make cart data available across the entire site
    """

    cart = request.session.get('cart', {})
    cart_items = sum(cart.values())

    return {
        'cart_item_count': cart_items,
    }