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
from api.models import TestServer
from api.models import TestRun
from api.models import TestSuite
from api.serializers import TestServerSerializer
from api.serializers import TestRunSerializer
from api.serializers import TestSuiteSerializer
from .testrun import run_test
import time
import logging

logger = logging.getLogger('apitest')


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


class RunTest(APIView):
    def post(self, request, format=None):
        testruns = []
        server = TestServer.objects.get(pk=request.data['serverId'])
        host = 'http://' + server.ip + ":" + str(server.port)
        for id in request.data['caseIds']:
            testcase = TestCase.objects.get(pk=id)
            url = host + testcase.uri
            # logger.info(url)
            test_result, response_data = run_test(testcase.method, url, testcase.params, testcase.expect)
            testrun = TestRun(caseid=testcase.id, casename=testcase.name,
                              runtime=time.strftime("%Y-%m-%d %H:%M:%S.%j", time.localtime()), request=testcase.params,
                              testresult=test_result, response=response_data)
            testrun.save()
            testruns.append(testrun)
        serializer = TestRunSerializer(testruns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, format=None):
        testrun = TestRun.objects.all().order_by('-id')
        serializer = TestRunSerializer(testrun, many='True')
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServerDetail(APIView):
    def get_object(self, pk):
        try:
            return TestServer.objects.get(pk=pk)
        except TestServer.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        testserver = self.get_object(pk)
        serializer = TestServerSerializer(testserver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        testserver = self.get_object(pk)
        serializer = TestServerSerializer(testserver)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        testserver = self.get_object(pk)
        testserver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServerList(APIView):
    def get(self, request, format=None):
        testserver = TestServer.objects.all()
        serializer = TestServerSerializer(testserver, many='True')
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # data = JSONParser().parse(request)
        serializer = TestServerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestSuiteList(APIView):
    def get(self, request, format=None):
        testsuite = TestSuite.objects.all()
        serializer = TestSuiteSerializer(testsuite, many='True')
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # data = JSONParser().parse(request)
        serializer = TestSuiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestModuleList(APIView):
    def get(self, request, format=None):
        testmodulelist = TestCase.objects.all()

