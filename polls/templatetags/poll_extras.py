from django import template


register = template.Library()


@register.filter()
def separate(number):
    '''put comma after 3 digits'''
    return F"{number:,}"

@register.simple_tag()
def products_lenght(category, enable_filter=False):
    if enable_filter:
        products_count = len(category.products.filter(is_enable=True))
    else:
        products_count = len(category.products.all())
    for sub_category in category.childs.all():
        products_count += products_lenght(sub_category, enable_filter)

    return products_count
