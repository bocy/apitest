from api.models import TestCase
from api.models import TestServer
from api.models import TestRun
from api.models import TestSuite
from api.models import SuiteResult
from rest_framework import serializers
from django.contrib.auth.models import User


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ('id', 'name', 'project', 'module', 'method', 'uri', 'params', 'expects',
                  'create', 'dataformat', 'headers')


class TestServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestServer
        fields = ('id', 'name', 'protocol', 'ip', 'port')


class TestRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRun
        fields = ('id', 'casename', 'testresult', 'request', 'response', 'runtime', 'testsuite')


class TestSuiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSuite
        fields = ('id', 'suitename', 'projects', 'caseids', 'casenames', 'serverid')


class SuiteResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiteResult
        fields = ('id', 'suitename', 'project', 'testresult', 'passnumber', 'failnumber', 'successrate', 'runtime')
