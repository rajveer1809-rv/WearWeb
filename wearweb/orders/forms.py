"""
Forms for orders app.
"""

from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    """
    Form for collecting checkout information.
    """

    class Meta:
        """
        Meta class for CheckoutForm.
        """
        model = Order
        fields = ['shipping_address', 'phone', 'payment_method']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
        }
