from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from . import api_processor
from rest_framework.response import Response
import logging

logging.getLogger().setLevel(logging.INFO)
# Create your views here.
class ApiCallView(APIView):

    def get(self,request,*args,**kwargs):
        logging.info(' API process start...')
        api_processor.dataProcess(execute=True)
        status_response = status.HTTP_200_OK
        json_response = {'process status': 'completed!'}

        return Response(json_response,status=status_response)
