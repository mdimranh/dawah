from django import template

register = template.Library()

@register.simple_tag
def percentage(like, dislike):
    print(like)
    print(dislike)
    return like
register.filter('percentage', percentage)