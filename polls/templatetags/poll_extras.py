from django import template


register = template.Library()


@register.filter()
def separate(number):
    '''put comma after 3 digits'''
    return F"{number:,}"

@register.simple_tag()
def products_lenght(category):
    products = len(category.products.all())
    for sub_category in category.childs.all():
        products += products_lenght(sub_category)

    return products

