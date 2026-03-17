"""
Models for orders app.
"""

from django.db import models
from core.models import User
from products.models import Product


class Order(models.Model):
    """
    Model representing an order.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Paid', 'Paid'),
            ('Shipped', 'Shipped'),
            ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled'),
        ],
        default="Pending"
    )

    shipping_address = models.TextField()

    phone = models.CharField(max_length=15)

    payment_method = models.CharField(max_length=20, choices=[
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ])

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"  # type: ignore


class OrderItem(models.Model):
    """
    Model representing an item in an order.
    """

    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        """
        Calculate subtotal for the item.
        """
        return self.price * self.quantity

    def __str__(self) -> str:
        return f"{self.product.name} x {self.quantity}"


class Dispute(models.Model):
    """
    Model representing a user dispute for an order.
    """

    order = models.ForeignKey(
        Order,
        related_name="disputes",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    subject = models.CharField(max_length=200)

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('Open', 'Open'),
            ('Resolved', 'Resolved'),
            ('Closed', 'Closed'),
        ],
        default="Open"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispute {self.id} for Order {self.order.id} - {self.status}"
