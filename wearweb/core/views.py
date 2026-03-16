"""
Views for core app.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from products.models import Product, Category, ProductLike
from .forms import SignupForm, LoginForm


def home_view(request):
    """
    Display home page with featured products and categories.
    """
    # Get featured products (latest 8 products)
    featured_products = Product.objects.all().order_by('-created_at')[:8]

    # Get parent categories
    parent_categories = Category.objects.filter(parent__isnull=True)

    # Get liked products for authenticated users
    liked_products = []
    if request.user.is_authenticated:
        liked_products = ProductLike.objects.filter(
            user=request.user
        ).values_list('product_id', flat=True)

    return render(request, "core/home.html", {
        'featured_products': featured_products,
        'parent_categories': parent_categories,
        'liked_products': list(liked_products),
    })


def signup_view(request):
    """
    Handle user signup.
    """
    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            if user.role == "vendor":
                return redirect("vendor_dashboard")

            elif user.role == "admin":
                return redirect("/admin/")

            return redirect("home")

    else:
        form = SignupForm()

    return render(
        request,
        "core/signup.html",
        {"form": form}
    )


def login_view(request):
    """
    Handle user login.
    """
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.role == "vendor":
                return redirect("vendor_dashboard")

            elif user.role == "admin":
                return redirect("/admin/")

            return redirect("home")

    return render(
        request,
        "core/login.html",
        {"form": form}
    )


def logout_view(request):
    """
    Handle user logout.
    """
    logout(request)

    return redirect("login")


def profile_view(request):
    """
    Display user profile.
    """
    return render(request, "core/profile.html")
