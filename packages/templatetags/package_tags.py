from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    value = dictionary.get(key)

    parts = value.split(' ')
    if len(parts) > 1:
        return parts[1]

    return value
