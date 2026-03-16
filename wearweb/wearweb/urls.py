"""
URL configuration for wearweb project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Home / authentication
    path('', include('core.urls')),

    # Products
    path('products/', include('products.urls')),

    # Cart
    path('cart/', include('cart.urls')),

    # Orders
    path('orders/', include('orders.urls')),

    # dashboard
    path('dashboard/', include('dashboard.urls')),
]


# Serve media files (product images) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)