from django import template
from account.models import User


register = template.Library()


@register.filter()
def separate(number):
    '''put comma after 3 digits'''
    return F"{number:,}"


@register.simple_tag()
def products_lenght(category, enable_filter=False, in_stock_filter=False):
    if enable_filter:
        products = category.products.filter(is_enable=True)
    else:
        products = category.products.all()
    if in_stock_filter in ["true", "True"]:
        products = [product for product in products if product.stock_count > 0]
        products_count = len(products)
    else:
        products_count = products.count()

    for sub_category in category.childs.all():
        products_count += products_lenght(sub_category,
                                          enable_filter, in_stock_filter)

    return products_count


@register.simple_tag()
def get_cart_item_quantity(product, user):
    """
    Return the quantity of this product in the user cart.
    """
    if isinstance(user, User):
        cart_item = product.carts.filter(
            cart__is_paid=False, cart__user_id=user.id).first()
        if cart_item is not None:
            return cart_item.quantity
    return 0
