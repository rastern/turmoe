import sys

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from engine import message, models, settings



# Create your views here.
class MockResponseView(View):
    def get_mock_response(self, request, *args, **kwargs):
        response = HttpResponse()

        # locate mocked response for this request
        mock = settings.MESSAGE_REPOSITORY.match(request)

        if getattr(mock, 'headers', None):
            for key, value in mock.headers.items():
                response[key] = value

        mock.set_state()
        response.status_code = getattr(mock, 'status_code', 200)
        response.write(mock.body)

        return response

    def get(self, request, *args, **kwargs):
        return self.get_mock_response(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get_mock_response(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.get_mock_response(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.get_mock_response(request, *args, **kwargs)
