from django import template

register = template.Library()


@register.filter
def get_current_path(request):
    return {
        'current_path': request.get_full_path()
    }