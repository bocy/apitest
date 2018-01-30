from api.models import TestCase
from api.models import TestServer
from api.models import TestRun
from rest_framework import serializers


class ApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ('id', 'name', 'module', 'method', 'uri', 'params', 'expect', 'create')


class TestServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestServer
        fields = ('id', 'name', 'ip', 'port')


class TestRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRun
        fields = ('id', 'casename', 'testresult', 'request', 'response', 'runtime')
