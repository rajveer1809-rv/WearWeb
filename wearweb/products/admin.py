from django.contrib import admin
from .models import Product, Category, ProductLike


class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model."""

    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)


admin.site.register(Product)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductLike)