from django.db import models
from core.models import User


class Category(models.Model):
    """
    Product category model with hierarchical support.
    """

    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )

    class Meta:
        """Meta class for Category."""
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name


class Product(models.Model):
    """
    Product model.
    """

    vendor = models.ForeignKey(User, on_delete=models.CASCADE)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )

    name = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(upload_to="products/")

    stock = models.IntegerField()

    # New fields for search and filtering
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class ProductLike(models.Model):
    """
    Model to track product likes by users.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class for ProductLike."""
        unique_together = ('user', 'product')

    def __str__(self) -> str:
        return f"{self.user.email} likes {self.product.name}"
