from django import template

register = template.Library()

@register.filter
def dict_key(value):
    return next(iter(value)) if isinstance(value, dict) else None

@register.filter
def get_item(dictionary, key):

    return list(dictionary.values())[0]