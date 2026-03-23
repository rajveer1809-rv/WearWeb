"""
URL configuration for orders app.
"""

from django.urls import path
from . import views

urlpatterns = [

    path("checkout/", views.checkout, name="checkout"),

    path("payment/<int:order_id>/", views.process_payment, name="process_payment"),

    path("verify-payment/", views.verify_payment, name="verify_payment"),

    path("receipt/<int:order_id>/", views.order_receipt, name="order_receipt"),

    path("cancel/<int:order_id>/", views.cancel_order, name="cancel_order"),

    path("dispute/<int:order_id>/", views.create_dispute, name="create_dispute"),

    path("success/", views.order_success, name="order_success"),

    path("my-orders/", views.my_orders, name="my_orders"),

    path("", views.my_orders, name="orders_home"),

]
