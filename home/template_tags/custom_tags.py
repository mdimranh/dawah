from django import template

register = template.Library()

@register.simple_tag
def percentage(like, dislike):
    print(like)
    print(dislike)
register.filter('percentage', percentage)