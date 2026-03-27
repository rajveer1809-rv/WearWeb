"""
Views for core app.
"""

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from products.models import Product, Category, ProductLike
from .forms import SignupForm, LoginForm
from django.http import HttpResponse


def health_check(request):
    """
    Simple health check view.
    """
    return HttpResponse("OK", status=200)


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
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.role == "vendor":
                return redirect("vendor_dashboard")
            elif user.role == "admin":
                return redirect("/admin/")
            return redirect("home")
        else:
            form.add_error(None, "Invalid email or password.")
            return render(request, "core/login.html", {"form": form})

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


def contact_us_view(request):
    """
    Display contact us page.
    """
    return render(request, "core/contectus.html")
