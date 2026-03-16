# Generated manually

"""
Migration to add order fields.
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Add shipping_address, phone, payment_method to Order and update status choices.
    """

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(
                choices=[
                    ('credit_card', 'Credit Card'),
                    ('debit_card', 'Debit Card'),
                    ('paypal', 'PayPal'),
                    ('cash_on_delivery', 'Cash on Delivery')
                ],
                default='cash_on_delivery',
                max_length=20
            ),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(
                choices=[
                    ('Pending', 'Pending'),
                    ('Paid', 'Paid'),
                    ('Shipped', 'Shipped'),
                    ('Delivered', 'Delivered'),
                    ('Cancelled', 'Cancelled')
                ],
                default='Pending',
                max_length=20
            ),
        ),
    ]
