"""
Views for orders app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from decimal import Decimal
import razorpay
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
    Handle payment processing using Razorpay.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'Paid':
        return redirect("order_success")

    amount_in_paise = int(order.total_price * 100)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Calculate transfers based on vendors
    transfers = []
    commission_rate = getattr(settings, 'PLATFORM_COMMISSION_PERCENTAGE', 10)

    vendor_amounts = {}
    for item in order.items.all():
        vendor = item.product.vendor
        if vendor.razorpay_account_id:
            vendor_id = vendor.razorpay_account_id
            item_total = item.price * item.quantity
            if vendor_id in vendor_amounts:
                vendor_amounts[vendor_id] += item_total
            else:
                vendor_amounts[vendor_id] = item_total

    for account_id, total_amount in vendor_amounts.items():
        commission = (Decimal(commission_rate) / Decimal(100)) * total_amount
        vendor_payout = total_amount - commission
        vendor_payout_paise = int(vendor_payout * 100)

        if vendor_payout_paise > 0:
            transfers.append({
                "account": account_id,
                "amount": vendor_payout_paise,
                "currency": "INR",
                "notes": {
                    "order_id": str(order.id)
                },
                "linked_account_notes": ["order_id"],
                "on_hold": 0
            })

    # Create Razorpay Order
    payment_data = {
        'amount': amount_in_paise,
        'currency': 'INR',
        'receipt': f'order_{order.id}',
    }

    if transfers:
        payment_data['transfers'] = transfers

    razorpay_order = client.order.create(data=payment_data)

    order.razorpay_order_id = razorpay_order['id']
    order.save()

    context = {
        "order": order,
        "razorpay_order_id": razorpay_order['id'],
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "amount_in_paise": amount_in_paise,
        "currency": "INR",
        "user": request.user
    }

    return render(request, "orders/process_payment.html", context)


@csrf_exempt
def verify_payment(request):
    """
    Verify Razorpay payment signature and update order status.
    """
    if request.method == "POST":
        data = request.POST
        payment_id = data.get('razorpay_payment_id', '')
        razorpay_order_id = data.get('razorpay_order_id', '')
        signature = data.get('razorpay_signature', '')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.status = 'Paid'
            order.razorpay_payment_id = payment_id
            order.razorpay_signature = signature
            order.save()

            # --- SEND RECEIPT EMAIL ---
            html_message = render_to_string("orders/emails/order_receipt.html", {"order": order})
            plain_message = strip_tags(html_message)
            send_mail(
                subject=f"WearWeb - Order #{order.id} Receipt",
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[order.user.email],
                html_message=html_message,
                fail_silently=True,
            )

            return redirect('order_success')
        except razorpay.errors.SignatureVerificationError:
            return render(request, "orders/payment_failed.html", {"error": "Payment signature verification failed."})
        except Order.DoesNotExist:
            return render(request, "orders/payment_failed.html", {"error": "Order not found."})

    return redirect('home')


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

        # --- SEND CANCELLATION EMAIL ---
        html_message = render_to_string("orders/emails/order_cancelled.html", {"order": order})
        plain_message = strip_tags(html_message)
        send_mail(
            subject=f"WearWeb - Order #{order.id} Cancelled",
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[order.user.email],
            html_message=html_message,
            fail_silently=True,
        )

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
