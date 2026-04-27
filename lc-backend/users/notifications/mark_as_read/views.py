from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .process_request import process_request

class MarkAsReadView(APIView):
    def post(self, request, user_id, notification_id):
        return process_request.post(user_id, notification_id)