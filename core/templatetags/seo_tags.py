from django import template

register = template.Library()


@register.simple_tag
def default_meta_title(context_title=None):
    return context_title or 'NEWMOON HOME'
