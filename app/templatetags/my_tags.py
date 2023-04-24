from django import template

register = template.Library()

@register.simple_tag
def my_tag(arg1, arg2):
    resultado = arg1 + arg2
    return resultado
