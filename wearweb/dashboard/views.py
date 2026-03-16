"""
Views for vendor dashboard.
"""

from django.shortcuts import render, redirect
from products.models import Product
from orders.models import OrderItem, Order


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
