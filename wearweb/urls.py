"""
URL configuration for wearweb project.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve


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


# Serve media files (product images) in production
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]