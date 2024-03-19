from django.shortcuts import render

from product.models import Category, Product, ProductColorVariant
from django.db.models import Count, Q, Sum


def index(request):
    # Get user.
    user = request.user
    # Get categories based on user permissions.
    categories = Category.access_controlled.filter_queryset_by_user_perms(
        user
    ).order_by("-id")
    # Get products based on user permissions.
    db_products = Product.access_controlled.filter_queryset_by_user_perms(
        user
    ).annotate(view_count=Count("viewers"))

    # Get the best selling product color variants.
    bs_product_colors = ProductColorVariant.objects.annotate(
        sold_count=Sum("carts__quantity", filter=Q(carts__cart__is_paid=True))).order_by("sold_count")
    
    # Get the best selling products.
    bs_products = reversed([
        product_color.product for product_color in bs_product_colors])
    
    # Remove the duplicated products.
    bs_products_without_duplicates = []
    for product in bs_products:
        if product not in bs_products_without_duplicates:
            bs_products_without_duplicates.append(product)

    context = {
        "categories": categories,
        "products": db_products,
        "best_selling_products": bs_products_without_duplicates,
    }
    return render(request, "index.html", context)


def header_component(request):
    return render(request, "components/header.html")


def footer_component(request):
    return render(request, "components/footer.html")
