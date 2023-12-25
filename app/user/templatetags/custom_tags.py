from django import template

register = template.Library()

@register.simple_tag
def get_field(fields):
    for field in fields:
        print(field)
        return field
