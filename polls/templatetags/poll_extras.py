from django import template


register = template.Library()


@register.filter()
def separate(number):
    '''put comma after 3 digits'''
    return F"{number:,}"



