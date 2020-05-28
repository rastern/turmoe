from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import views
from engine import message



BODY404 = """
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL /admin/version was not found on this server.</p>
</body></html>
"""


# Create your views here.
class ApiView(views.APIView):
    permission_classes = []

    def get_response(self, request, *args, **kwargs):
        response = HttpResponse()
        mock = message.find(request)

        if mock:
            if mock.get('headers'):
                for key, value in mock['headers'].items():
                    response[key] = value

            response.status_code = mock.get('status_code', 200)
            response.write(mock['body'])
        else:
            response.status_code = 404
            response.write(BODY404)

        return response

    def get(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.get_response(request, *args, **kwargs)
