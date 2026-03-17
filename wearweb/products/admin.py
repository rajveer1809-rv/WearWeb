from django.contrib import admin
from .models import Product, Category, ProductLike, Review


class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model."""

    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    """Admin for Review model."""

    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Product)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductLike)
admin.site.register(Review, ReviewAdmin)