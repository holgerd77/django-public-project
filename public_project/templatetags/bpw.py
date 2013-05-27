from django import template

register = template.Library()

@register.filter
def modelname(object):
    if hasattr(object, '__class__'):
        return object.__class__.__name__.lower()
    else:
        return ""
    