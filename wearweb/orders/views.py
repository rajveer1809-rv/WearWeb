"""
Views for orders app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm, DisputeForm


@login_required
def order_receipt(request, order_id):
    """
    Display order receipt.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/receipt.html", {"order": order})


@login_required
def create_dispute(request, order_id):
    """
    Create a dispute for an order.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == "POST":
        form = DisputeForm(request.POST)
        if form.is_valid():
            dispute = form.save(commit=False)
            dispute.order = order
            dispute.user = request.user
            dispute.save()
            return redirect("my_orders")
    else:
        form = DisputeForm()

    return render(request, "orders/create_dispute.html", {
        "order": order,
        "form": form
    })


@login_required
def checkout(request):
    """
    Handle checkout process.
    """
    cart = Cart.objects.get_or_create(user=request.user)[0]  # type: ignore

    items = cart.items.all()

    if not items:
        return redirect("cart_page")

    total = sum(item.subtotal() for item in items)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Save user details if not set
            user = request.user
            if not user.phone:
                user.phone = form.cleaned_data['phone']
            if not user.address:
                user.address = form.cleaned_data['shipping_address']
            user.save()

            order = form.save(commit=False)
            order.user = user
            order.total_price = total
            order.save()

            for item in items:  # pylint: disable=too-many-branches
                OrderItem.objects.create(  # type: ignore  # type: ignore
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            items.delete()

            # After checkout, process payment
            return redirect("process_payment", order_id=order.id)
    else:
        form = CheckoutForm(initial={
            'phone': request.user.phone,
            'shipping_address': request.user.address,
        })

    return render(request, "orders/checkout.html", {
        "items": items,
        "total": total,
        "form": form
    })


@login_required
def process_payment(request, order_id):
    """
    Handle payment processing.
    """
    order = Order.objects.get(id=order_id, user=request.user)  # type: ignore

    if request.method == "POST":
        # Simulate payment processing
        order.status = 'Paid'
        order.save()
        return redirect("order_success")

    return render(request, "orders/process_payment.html", {
        "order": order
    })


@login_required
def order_success(request):
    """
    Display order success page.
    """
    return render(request, "orders/order_success.html")


@login_required
def cancel_order(request, order_id):
    """
    Cancel an order if it's pending or paid.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status in ['Pending', 'Paid']:
        order.status = 'Cancelled'
        order.save()
    return redirect('my_orders')


@login_required
def my_orders(request):
    """
    Display user's orders.
    """
    orders = Order.objects.filter(user=request.user)  # type: ignore

    return render(request, "orders/my_orders.html", {
        "orders": orders
    })
