from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from api.models import TestCase
from api.serializers import TestCaseSerializer
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from api.models import TestServer
from api.models import TestRun
from api.models import TestSuite
from api.models import SuiteResult
from api.serializers import TestServerSerializer
from api.serializers import TestRunSerializer
from api.serializers import TestSuiteSerializer
from api.serializers import SuiteResultSerializer
from .testrun import run_test
import time, os, binascii
import logging
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import utils

logger = logging.getLogger('apitest')


# Create your views here.
# class CaseViewSet(viewsets.ModelViewSet):
#     queryset = TestCase.objects.all().order_by('create')
#     serializer_class = ApiSerializer


class CaseList(APIView):
    def get(self, request, format=None):
        # testcase = TestCase.objects.all()
        page_size = request.query_params.get('size') or 20
        offset = request.query_params.get('offset') or 1
        case_name = request.query_params.get('name') or ''
        project = request.query_params.get('project') or ''
        if project == 'all':
            project = ''
        testcase = TestCase.objects.filter(name__icontains=case_name, project__contains=project)
        paginator = Paginator(testcase, page_size)
        _total = len(testcase)
        data = paginator.page(offset).object_list
        serializer = TestCaseSerializer(data, many='True')
        resp_dict = {
            'total': _total,
            'data': serializer.data
        }
        # serializer = ApiSerializer(data, many='True')
        return Response(resp_dict)

    def post(self, request, format=None):
        # data = JSONParser().parse(request)
        serializer = TestCaseSerializer(data=request.data)
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
        serializer = TestCaseSerializer(testcase)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        testcase = self.get_object(pk)
        # data = JSONParser().parse(testcase)
        serializer = TestCaseSerializer(testcase, data=request.data)
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
        host = server.protocol + "://" + server.ip + ":" + str(server.port)
        for id in request.data['caseIds']:
            testcase = TestCase.objects.get(pk=id)
            url = host + testcase.uri
            # logger.info(url)
            test_result, response_data = run_test(testcase.method, url, testcase.dataformat, testcase.params,
                                                  testcase.expects, testcase.headers)
            testrun = TestRun(caseid=testcase.id, casename=testcase.name,
                              runtime=time.strftime("%Y-%m-%d %H:%M:%S.%j", time.localtime()), request=testcase.params,
                              testresult=test_result, response=response_data)
            testrun.save()
            testruns.append(testrun)
        serializer = TestRunSerializer(testruns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, format=None):
        # testrun = TestRun.objects.all().order_by('-id')
        page_size = request.query_params.get('size')
        offset = request.query_params.get('offset')
        testresult = request.query_params.get('testresult') or ''
        name = request.query_params.get('name') or ''
        testsuite = request.query_params.get('testsuite') or ''
        testrun = TestRun.objects.filter(casename__contains=name, testresult__contains=testresult,
                                         testsuite__contains=testsuite).order_by('-id')
        paginator = Paginator(testrun, page_size)
        _total = len(testrun)
        data = paginator.page(offset).object_list
        serializer = TestRunSerializer(data, many='True')
        resp_dict = {
            'total': _total,
            'data': serializer.data
        }
        # serializer = TestRunSerializer(testrun, many='True')
        return Response(resp_dict, status=status.HTTP_200_OK)


class RunSuiteTest(APIView):
    def get(self, request, *args, **kwargs):
        suiteResult = SuiteResult.objects.all().order_by('-id')
        serializer = SuiteResultSerializer(suiteResult, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        pass_count = 0
        fail_count = 0
        success_rat = 0
        suite_result = 'Pass'
        suiteid = request.data.get('id')
        test_suite = TestSuite.objects.get(pk=suiteid)
        test_server = TestServer.objects.get(pk=test_suite.serverid)
        host = 'http://' + test_server.ip + ':' + str(test_server.port)
        for id in request.data['caseids']:
            testcase = TestCase.objects.get(pk=id)
            url = host + testcase.uri
            # logger.info(url)
            test_result, response_data = run_test(testcase.method, url, testcase.params, testcase.expect, testcase.headers)
            testrun = TestRun(caseid=testcase.id, casename=testcase.name,
                              runtime=time.strftime("%Y-%m-%d %H:%M:%S.%j", time.localtime()), request=testcase.params,
                              testresult=test_result, response=response_data)
            testrun.save()
            if test_result == 'Pass':
                pass_count += 1
            else:
                fail_count += 1
        if fail_count > 0:
            suite_result = 'Fail'
        success_rat = pass_count/(pass_count+fail_count) * 100
        suiteResult = SuiteResult(suitename=test_suite.suitename, project=test_suite.projects,
                                  testresult=suite_result, passnumber=pass_count, failnumber=fail_count,
                                  successrate=success_rat, runtime=time.strftime("%Y-%m-%d %H:%M:%S.%j", time.localtime()))
        suiteResult.save()
        serializer = SuiteResultSerializer(suiteResult)
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
        caseids = []
        casenames = []
        suite_name = request.data.get('suiteName')
        projects = request.data.get('project') or ''
        serverid = request.data.get('serverId')
        if len(request.data.get('testcases')) > 0:
            caseids += request.data.get('testcases')
        for project in projects:
            testcases = TestCase.objects.values('id').filter(project=project)
            for test in testcases:
                caseids.append(test.get('id'))
        for id in caseids:
            tc = TestCase.objects.get(id=id)
            casenames.append(tc.name)
        testsuite = TestSuite(suitename=suite_name, projects=projects, caseids=caseids, casenames=casenames,
                              serverid=serverid)
        testsuite.save()
        return Response('{ "code": 0,"msg":"Test Suite create success" }', status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        testsuit = TestSuite.objects.get(pk=pk)
        testsuit.delete()
        return Response('{ "code": 0,"msg":"Test Suite delete success" }', status=status.HTTP_200_OK)


class ProjectList(APIView):
    def get(self, request, format=None):
        projects = TestCase.objects.values('project').annotate(Count('id'))
        data_list = ['all']
        for i in projects:
            data_list.append(i.get('project'))
        return Response(data_list, status=status.HTTP_200_OK)


class ModuleList(APIView):
    def get(self, request,  *args, **kwargs):
        project = request.query_params.get('project')
        modules = TestCase.objects.values('module').annotate(Count('id'))
        modules_list = []
        for m in modules:
            modules_list.append(m.get('module'))
        return Response(modules_list, status=status.HTTP_200_OK)


class FindModuleByProject(APIView):
    def get(self, request,  *args, **kwargs):
        project = request.query_params.get('project')
        modules = TestCase.objects.values('module').filter(project=project).annotate(Count('module'))
        modules_list = []
        for m in modules:
            modules_list.append(m.get('module'))
        return Response(modules_list, status=status.HTTP_200_OK)


class FindTestcaseByProjectAndModule(APIView):
    def get(self, request,  *args, **kwargs):
        project = request.query_params.get('project')
        module = request.query_params.get('module')
        testcases = TestCase.objects.filter(project=project, module=module)
        serializer = TestCaseSerializer(testcases, many=True)
        # testcase_list = []
        # for testcase in testcases:
        #     testcase_list.append(testcase.name)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Login(APIView):
    def get(self, request, *args, **kwargs):
        # username = request.data.get('username')
        # password = request.data.get('password')
        username = request.query_params.get('username')
        password = request.query_params.get('password')
        # user = authenticate(request, username=username, password=password)
        res = {'code': 0, 'msg': None}
        data = {}
        if username == 'admin' and password == 'admin':
            # login(request, user)
            token = binascii.hexlify(os.urandom(20)).decode()
            data['token'] = token
            res['data'] = data
            res['msg'] = '登录成功！'
            return JsonResponse(res)
            # return Response(res, status=status.HTTP_200_OK)
        else:
            res['code'] = 1001
            res['msg'] = '登录失败！'
            return JsonResponse(res)
            # return Response(res, status=status.HTTP_401_UNAUTHORIZED)


# @login_required
class GetUserInfo(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('name')
        is_exsist = User.objects.filter(username=username)
        if is_exsist:
            return Response({"code": 0, "data": {"roles":["admin"],"name":"admin","avatar":"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1528891405014&di=61a32ac27642006c406e264dd2ee55b6&imgtype=0&src=http%3A%2F%2Fimg2.zol.com.cn%2Fup_pic%2F20121025%2Fz1Ovnapsa1Cg.gif"}})
            # return Response({"code": 0, "data": {"roles":["admin"],"name":"admin","avatar":"https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"}})
        else:
            return Response({"code": 20001, "msg": '用户不存在'})


class Logout(APIView):
    def post(self, request, format=None):
        return Response({"code": 0, "msg": '登出成功'}, status=status.HTTP_200_OK)


class Idcard(APIView):
    def get(self, request, *args, **kwargs):
        area_code = request.query_params.get('areacode')
        age = request.query_params.get('age')
        sex = request.query_params.get('sex')
        idcards = []
        for x in range(5):
            idcard = utils.gen_id_card(area_code, age, sex)
            idcards.append(idcard)
        return Response({"code": 0, "data": idcards}, status=status.HTTP_200_OK)

