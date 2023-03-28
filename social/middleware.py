# from django import http
# from urllib.parse import quote
# from django import urls
# from django.conf import settings
# from django.utils.deprecation import MiddlewareMixin
# from django.shortcuts import redirect


# class AppendOrRemoveSlashMiddleware(MiddlewareMixin):
#     """Like django's built in APPEND_SLASH functionality, but also works in
#     reverse. Eg. will remove the slash if a slash-appended url won't resolve,
#     but its non-slashed counterpart will.
#     Additionally, if a 404 error is raised within a view for a non-slashed url,
#     and APPEND_SLASH is True, and the slash-appended url resolves, the
#     middleware will redirect. (The default APPEND_SLASH behaviour only catches
#     Resolver404, so wouldn't work in this case.)
#     See gregbrown.co.nz/code/append-or-remove-slash/ for more information."""

#     def process_request(self, request):
#         """Returns a redirect if adding/removing a slash is appropriate. This
#         works in the same way as the default APPEND_SLASH behaviour but in
#         either direction."""
#         # check if the url is valid
#         new_path = ""
#         urlconf = getattr(request, 'urlconf', None)
#         if (request.path_info.endswith('/') == False):
#             new_path = request.path_info + '/'
#         print(request.method)
#         if _is_valid_path(new_path, urlconf):
#             # if the new url is valid, redirect to it
#             http.HttpResponsePermanentRedirect(generate_url(request, new_path))

#     # def process_response(self, request, response):
#     #     """If a 404 is raised within a view, try appending/removing the slash
#     #     (based on the  setting) and redirecting if the new url is
#     #     valid."""

#     #     if response.status_code == 404:
#     #         if not request.path_info.endswith('/') and settings.APPEND_SLASH:
#     #             new_path = request.path_info + '/'
#     #         elif request.path_info.endswith('/') and not settings.APPEND_SLASH:
#     #             new_path = request.path_info[:-1]
#     #         else:
#     #             new_path = None

#     #         if new_path:
#     #             urlconf = getattr(request, 'urlconf', None)
#     #             if _is_valid_path(new_path, urlconf):
#     #                 return http.HttpResponsePermanentRedirect(
#     #                     generate_url(request, new_path))
#     #     return response


# def generate_url(request, path):
#     if request.get_host():
#         new_url = "%s://%s%s" % ('http',
#                                  request.get_host(),
#                                  quote(path))
#     else:
#         new_url = quote(path)
#     return new_url


# def _is_valid_path(path, urlconf=None):
#     """
#     Returns True if the given path resolves against the default URL resolver,
#     False otherwise.
#     """
#     try:
#         urls.resolve(path, urlconf)
#         return True
#     except urls.Resolver404:
#         return False


from django.http import HttpResponsePermanentRedirect, HttpRequest
from django.core.handlers.base import BaseHandler
from django.middleware.common import CommonMiddleware
from django.utils.http import escape_leading_slashes
from django.conf import settings


class HttpSmartRedirectResponse(HttpResponsePermanentRedirect):
    pass


class CommonMiddlewareAppendSlashWithoutRedirect(CommonMiddleware):
    """ This class converts HttpSmartRedirectResponse to the common response
            of Django view, without redirect. This is necessary to match status_codes
            for urls like /url?q=1 and /url/?q=1. If you don't use it, you will have 302
            code always on pages without slash.
    """
    response_redirect_class = HttpSmartRedirectResponse

def __init__(self, *args, **kwargs):
    # create django request resolver
    self.handler = BaseHandler()

    # prevent recursive includes
    old = settings.MIDDLEWARE
    name = self.__module__ + '.' + self.__class__.__name__
    settings.MIDDLEWARE = [i for i in settings.MIDDLEWARE if i != name]

    self.handler.load_middleware()

    settings.MIDDLEWARE = old
    super(CommonMiddlewareAppendSlashWithoutRedirect, self).__init__(*args, **kwargs)

def get_full_path_with_slash(self, request):
    """ Return the full path of the request with a trailing slash appended
        without Exception in Debug mode
    """
    new_path = request.get_full_path(force_append_slash=True)
    # Prevent construction of scheme relative urls.
    new_path = escape_leading_slashes(new_path)
    return new_path

def process_response(self, request, response):
    response = super(CommonMiddlewareAppendSlashWithoutRedirect, self).process_response(request, response)

    if isinstance(response, HttpSmartRedirectResponse):
        if not request.path.endswith('/'):
            request.path = request.path + '/'
        # we don't need query string in path_info because it's in request.GET already
        request.path_info = request.path
        response = self.handler.get_response(request)

    return response