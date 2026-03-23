from django.urls import path
from . import views

urlpatterns = [

    path("vendor/", views.vendor_dashboard, name="vendor_dashboard"),
    
    path("admin/", views.admin_dashboard, name="admin_dashboard"),

    path("disputes/", views.manage_disputes, name="manage_disputes"),

    path("resolve-dispute/<int:dispute_id>/", views.resolve_dispute, name="resolve_dispute"),

    path("deactivate-user/<int:user_id>/", views.deactivate_user, name="deactivate_user"),

]