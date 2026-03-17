from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg, Count, Q
from .models import Product, Category, ProductLike, Review
from .forms import ProductForm, ReviewForm


def product_list(request):
    """Display products with category filtering, search, and filters."""
    products = Product.objects.all()
    selected_category = None
    parent_categories = Category.objects.filter(parent__isnull=True)
    liked_products = []

    # Get search and filter parameters
    search_query = request.GET.get('search', '').strip()
    selected_color = request.GET.get('color', '').strip()
    selected_size = request.GET.get('size', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        # Get products from selected category and its subcategories
        products = products.filter(
            category__in=selected_category.children.all() | Category.objects.filter(id=selected_category.id)
        )

    # Apply search filter
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Apply color filter
    if selected_color:
        products = products.filter(color__iexact=selected_color)

    # Apply size filter
    if selected_size:
        products = products.filter(size__iexact=selected_size)

    # Apply price filters
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Get available colors and sizes for filter options
    available_colors = Product.objects.values_list('color', flat=True).distinct().exclude(color__isnull=True).exclude(color='').order_by('color')
    available_sizes = Product.objects.values_list('size', flat=True).distinct().exclude(size__isnull=True).exclude(size='').order_by('size')

    if request.user.is_authenticated:
        liked_products = ProductLike.objects.filter(
            user=request.user
        ).values_list('product_id', flat=True)  # type: ignore

    return render(request, "products/product_list.html", {
        "products": products,
        "parent_categories": parent_categories,
        "selected_category": selected_category,
        "liked_products": list(liked_products),
        "search_query": search_query,
        "selected_color": selected_color,
        "selected_size": selected_size,
        "min_price": min_price,
        "max_price": max_price,
        "available_colors": available_colors,
        "available_sizes": available_sizes,
    })


def product_detail(request, pk):

    product = get_object_or_404(Product, id=pk)
    is_liked = False
    user_review = None
    review_form = ReviewForm()

    if request.user.is_authenticated:
        is_liked = ProductLike.objects.filter(
            user=request.user, product=product
        ).exists()  # type: ignore
        user_review = Review.objects.filter(
            user=request.user, product=product
        ).first()

    # Handle review submission
    if request.method == "POST" and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', pk=product.id)

    # Get all reviews for the product
    reviews = Review.objects.filter(product=product)
    
    # Calculate average rating
    rating_stats = reviews.aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('id')
    )
    avg_rating = rating_stats['avg_rating'] or 0
    total_reviews = rating_stats['total_reviews'] or 0

    return render(request, "products/product_detail.html", {
        "product": product,
        "is_liked": is_liked,
        "reviews": reviews,
        "avg_rating": round(avg_rating, 1),
        "total_reviews": total_reviews,
        "user_review": user_review,
        "review_form": review_form,
    })


@login_required
def add_product(request):

    if request.user.role != "vendor":
        return redirect("product_list")

    form = ProductForm(request.POST or None, request.FILES or None)

    if form.is_valid():

        product = form.save(commit=False)
        product.vendor = request.user
        product.save()

        return redirect("product_list")

    return render(request, "products/add_product.html", {
        "form": form
    })


@login_required
def update_product(request, pk):

    product = get_object_or_404(Product, id=pk)

    if product.vendor != request.user:
        return redirect("product_list")

    form = ProductForm(
        request.POST or None,
        request.FILES or None,
        instance=product
    )

    if form.is_valid():
        form.save()
        return redirect("product_detail", pk=product.id)

    return render(request, "products/update_product.html", {
        "form": form
    })


@login_required
def delete_product(request, pk):

    product = get_object_or_404(Product, id=pk)

    if product.vendor != request.user:
        return redirect("product_list")

    product.delete()

    return redirect("product_list")

@login_required
def vendor_products(request):

    products = Product.objects.filter(vendor=request.user)

    return render(request, "products/vendor_products.html", {
        "products": products
    })


@login_required
def like_product(request, product_id):
    """
    Toggle like status for a product.
    """
    product = get_object_or_404(Product, id=product_id)

    like_obj, created = ProductLike.objects.get_or_create(
        user=request.user, product=product
    )  # type: ignore

    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked})

    return redirect('product_detail', pk=product_id)


@login_required
def liked_products(request):
    """
    Display all products liked by the current user.
    """
    liked_products = Product.objects.filter(
        likes__user=request.user
    ).distinct()  # type: ignore

    return render(request, "products/liked_products.html", {
        "products": liked_products,
    })
