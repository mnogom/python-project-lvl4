"""Shortcuts."""


def back_url(request, default='index'):
    _url = request.META.get('HTTP_REFERER')
    return _url if _url else default
