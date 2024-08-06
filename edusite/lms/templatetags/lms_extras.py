from django import template
from lms.models import Category,Course

register = template.Library()

@register.filter
def get_by_cat_name(value,arg):
    return value.filter(category__name__contains=arg)[:6]
