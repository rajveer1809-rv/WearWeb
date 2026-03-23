"""
Views for vendor dashboard.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from products.models import Product
from orders.models import OrderItem, Order, Dispute
from core.models import User


@login_required
def vendor_dashboard(request):
    """
    Display vendor dashboard with sales and product statistics.
    """

    if request.user.role != "vendor":
        return redirect("product_list")

    products = Product.objects.filter(vendor=request.user)

    order_items = OrderItem.objects.filter(product__vendor=request.user)

    total_sales = sum(item.price * item.quantity for item in order_items)

    # Additional stats
    recent_orders = (Order.objects.filter(
        items__product__vendor=request.user
    ).distinct().order_by('-created_at')[:5])  # type: ignore

    context = {
        "products": products,
        "order_items": order_items,
        "total_sales": total_sales,
        "total_products": products.count(),
        "total_orders": order_items.count(),
        "recent_orders": recent_orders,
    }

    return render(request, "dashboard/vendor_dashboard.html", context)


@login_required
def admin_dashboard(request):
    """
    Display admin dashboard monitoring sales, users, and inventory.
    """
    if request.user.role != "admin":
        return redirect("product_list")

    # Monitor Sales
    # All paid or delivered orders
    successful_orders = Order.objects.filter(status__in=['Paid', 'Delivered'])  # type: ignore
    total_platform_sales = sum(order.total_price for order in successful_orders)
    
    # Monitor Users
    total_users = User.objects.count()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_users_last_30_days = User.objects.filter(created_at__gte=thirty_days_ago).count()

    # Monitor Inventory
    # Find low stock products
    low_stock_products = Product.objects.filter(stock__lt=10).order_by('stock')[:10]  # type: ignore

    # Active Disputes
    active_disputes = Dispute.objects.filter(status='Open').order_by('-created_at')  # type: ignore

    context = {
        "total_platform_sales": total_platform_sales,
        "total_users": total_users,
        "new_users_last_30_days": new_users_last_30_days,
        "low_stock_products": low_stock_products,
        "active_disputes": active_disputes,
        "successful_orders_count": successful_orders.count()
    }

    return render(request, "dashboard/admin_dashboard.html", context)


@login_required
def manage_disputes(request):
    """
    Admin view for managing all disputes.
    """
    if request.user.role != "admin":
        return redirect("product_list")

    disputes = Dispute.objects.all().order_by('-created_at')  # type: ignore

    return render(request, "dashboard/manage_disputes.html", {
        "disputes": disputes
    })


@login_required
def resolve_dispute(request, dispute_id):
    """
    Admin action to resolve a dispute.
    """
    if request.user.role != "admin":
        return redirect("product_list")

    dispute = get_object_or_404(Dispute, id=dispute_id)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "resolve":
            dispute.status = "Resolved"
        elif action == "close":
            dispute.status = "Closed"
        dispute.save()
    
    return redirect("manage_disputes")


@login_required
def deactivate_user(request, user_id):
    """
    Admin action to deactivate user violating platform policy.
    """
    if request.user.role != "admin":
        return redirect("product_list")

    user_to_deactivate = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user_to_deactivate.is_active = False
        user_to_deactivate.save()

    return redirect("manage_disputes")
