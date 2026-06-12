from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f"/media/mailing/images/{path}"
    else:
        return "#"
