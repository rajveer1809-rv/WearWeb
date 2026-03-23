from django import forms
from .models import Product, Category, Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(
                choices=Review.RATING_CHOICES,
                attrs={'class': 'form-check-input'}
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Share your experience with this product...'
                }
            ),
        }

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(children__isnull=True),
        empty_label="Select Subcategory",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Color choices for better UX
    COLOR_CHOICES = [
        ('', 'Select Color'),
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Green', 'Green'),
        ('Black', 'Black'),
        ('White', 'White'),
        ('Gray', 'Gray'),
        ('Pink', 'Pink'),
        ('Purple', 'Purple'),
        ('Yellow', 'Yellow'),
        ('Orange', 'Orange'),
        ('Brown', 'Brown'),
        ('Beige', 'Beige'),
        ('Navy', 'Navy'),
        ('Maroon', 'Maroon'),
        ('Other', 'Other'),
    ]

    # Size choices for clothing
    SIZE_CHOICES = [
        ('', 'Select Size'),
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('3XL', '3XL'),
        ('4XL', '4XL'),
        ('Free Size', 'Free Size'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    ]

    color = forms.ChoiceField(
        choices=COLOR_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    size = forms.ChoiceField(
        choices=SIZE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'color', 'size', 'image', 'stock']