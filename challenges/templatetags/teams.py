from django import template

register = template.Library()

@register.simple_tag
def teams(resolutions):
    return [resolution.team for resolution in resolutions]
