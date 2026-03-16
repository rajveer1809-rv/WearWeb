from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from products.models import Product


def add_to_cart(request, pk):

    product = get_object_or_404(Product, id=pk)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1
        )

    return redirect("cart_page")


def cart_page(request):

    cart, created = Cart.objects.get_or_create(user=request.user)

    items = cart.items.all()

    total = sum(item.subtotal() for item in items)

    return render(request, "cart/cart_page.html", {
        "items": items,
        "total": total
    })


def increase_quantity(request, pk):

    item = get_object_or_404(CartItem, id=pk)

    item.quantity += 1
    item.save()

    return redirect("cart_page")


def decrease_quantity(request, pk):

    item = get_object_or_404(CartItem, id=pk)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart_page")


def remove_item(request, pk):

    item = get_object_or_404(CartItem, id=pk)

    item.delete()

    return redirect("cart_page")