from django.urls import path
from . import views

urlpatterns = [

    path("", views.product_list, name="product_list"),

    path("<int:pk>/", views.product_detail, name="product_detail"),

    path("add/", views.add_product, name="add_product"),

    path("update/<int:pk>/", views.update_product, name="update_product"),

    path("delete/<int:pk>/", views.delete_product, name="delete_product"),

    path("vendor/", views.vendor_products, name="vendor_products"),

    path("like/<int:product_id>/", views.like_product, name="like_product"),

    path("liked/", views.liked_products, name="liked_products"),

]
