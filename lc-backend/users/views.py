from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .process_request import process_request

class testView(APIView):
    def get(self, request, pk=None):
        return process_request.get(request, id=pk)
    def post(self, request):
        return process_request.post(request)