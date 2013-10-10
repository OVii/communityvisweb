__author__ = 'eamonnmaguire'

from django.conf import settings

def url_prepender(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'URL_PREPENDER': settings.URL_PREPENDER}
