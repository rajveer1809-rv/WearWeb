from django.urls import path
from . import views

urlpatterns = [

    path("", views.cart_page, name="cart_page"),

    path("add/<int:pk>/", views.add_to_cart, name="add_to_cart"),

    path("increase/<int:pk>/", views.increase_quantity, name="increase_quantity"),

    path("decrease/<int:pk>/", views.decrease_quantity, name="decrease_quantity"),

    path("remove/<int:pk>/", views.remove_item, name="remove_item"),

]