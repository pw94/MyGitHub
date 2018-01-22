from django import template

register = template.Library()


@register.simple_tag
def call_method(obj, name, user):
    method = getattr(obj, name)
    return method(user)


@register.filter
def not_none(value):
    return value if value else str()
