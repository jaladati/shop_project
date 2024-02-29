from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from product.models import ProductColorVariant
from .models import Cart, CartItem


@require_GET
@login_required
def add_product_to_cart(request):
    # Get id and quantity.
    id = request.GET.get("id")
    quantity = request.GET.get("quantity", 1)

    # Are id and quantity integers?
    if not id.isdigit() or not quantity.isdigit():
        response = {"text": "مقداری نامعتبر وارد شده است",
                    "icon": "error", "position": "center"}
        return JsonResponse(response)
    quantity = int(quantity)

    # Find product.
    product = ProductColorVariant.objects.filter(
        product__is_enable=True, id=id).first()
    # If the product is not found, Return error.
    if product is None:
        response = {"text": "محصولی یافت نشد", "icon": "error",
                    "position": "center"}
        return JsonResponse(response)
    # Validate the entered quantity.
    if quantity < 1 or quantity > product.stock_count:
        response = {"text": "تعداد وارد شده نامعتبر است",
                    "icon": "error", "position": "center"}
        return JsonResponse(response)

    user = request.user

    # Get the user's open cart if it exists, otherwise create it and then get it.
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    # Get the current product cart-item if it exists, otherwise
    # create it and then get it.
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={"quantity": quantity})

    if created:
        response = {"text": "محصول با موفقیت به سبد خرید شما افزوده شد",
                    "icon": "success", "position": "top-end"}
    else:
        # Save the changes.
        cart_item.quantity = quantity
        cart_item.save()

        response = {"text": "تعداد محصول در سبد خرید با موفقیت تغییر یافت",
                    "icon": "success", "position": "top-end"}

    # Render the product colors area for update the item quantities.
    colors = product.product.in_stock_color_variants()
    product_colors_area = render_to_string(
        "components/product_colors.html", {"colors": colors}, request)
    response["product_colors_area"] = product_colors_area

    return JsonResponse(response)
