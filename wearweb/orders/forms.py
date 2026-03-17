"""
Forms for orders app.
"""

from django import forms
from .models import Order, Dispute


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


class DisputeForm(forms.ModelForm):
    """
    Form for users to submit a dispute for an order.
    """

    class Meta:
        """
        Meta class for DisputeForm.
        """
        model = Dispute
        fields = ['subject', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
