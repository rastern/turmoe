from engine import settings



class UrlPatternUpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if settings.API_DYNAMIC_URLS and \
        request.path.strip('/').startswith(settings.API_BASE_PATH):
            request.urlconf = 'engine.urls'

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
