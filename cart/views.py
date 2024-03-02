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
    try:
        id = int(request.GET.get("id"))
        quantity = int(request.GET.get("quantity", 1))
    # If id or quantity is not numeric return error.
    except:
        response = {"text": "مقداری نامعتبر وارد شده است",
                    "icon": "error", "position": "center"}
        return JsonResponse(response)

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
                    "icon": "success", "position": "center"}
    else:
        # Save the changes.
        cart_item.quantity = quantity
        cart_item.save()

        response = {"text": "تعداد محصول در سبد خرید با موفقیت تغییر یافت",
                    "icon": "success", "position": "center",
                    "cart_item_total_price": cart_item.total_price(),
                    "cart_total_discounted_price": cart.total_discounted_price(),
                    "cart_total_discounted": cart.total_discounted(),
                    "cart_total_price": cart.total_price()}

    # Render the product colors area for update the item quantities.
    colors = product.product.in_stock_color_variants()
    product_colors_area = render_to_string(
        "components/product_colors.html", {"colors": colors}, request)
    response["product_colors_area"] = product_colors_area

    return JsonResponse(response)


@require_GET
@login_required
def remove_product_from_cart(request):
    # Get cart item.
    user = request.user
    item_id = request.GET.get("item_id")
    cart_item = CartItem.objects.filter(
        cart__is_paid=False, cart__user_id=user.id, id=item_id).first()

    # Remove item if exists.
    if cart_item is not None:
        cart_item.delete()
        cart = cart_item.cart
        response = {"text": "محصول با موفقیت از سبد خرید حذف شد",
                    "icon": "success", "position": "center",
                    "cart_total_discounted_price": cart.total_discounted_price(),
                    "cart_total_discounted": cart.total_discounted(),
                    "cart_total_price": cart.total_price()}
        return JsonResponse(response)

    # Return error.
    response = {"text": "محصول یافت نشد",
                "icon": "error", "position": "center"}
    return JsonResponse(response)
