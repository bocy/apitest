from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from api.models import TestCase
from api.serializers import ApiSerializer
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from requests import request


# Create your views here.
# class CaseViewSet(viewsets.ModelViewSet):
#     queryset = TestCase.objects.all().order_by('create')
#     serializer_class = ApiSerializer


class CaseList(APIView):
    def get(self, request, format=None):
        testcase = TestCase.objects.all()
        serializer = ApiSerializer(testcase, many='True')
        return Response(serializer.data)

    def post(self, request, format=None):
        # data = JSONParser().parse(request)
        serializer = ApiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CaseDetail(APIView):
    def get_object(self, pk):
        try:
            return TestCase.objects.get(pk=pk)
        except TestCase.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        testcase = self.get_object(pk)
        serializer = ApiSerializer(testcase)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        testcase = self.get_object(pk)
        # data = JSONParser().parse(testcase)
        serializer = ApiSerializer(testcase, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        testcase = self.get_object(pk)
        testcase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TestRun(APIView):
    def get_object(self, pk):
        try:
            return TestCase.objects.get(pk=pk)
        except TestCase.DoesNotExist:
            raise Http404

    def post(self, pk):
        testcase = self.get_object(pk)
        resp = request(testcase.method,)
