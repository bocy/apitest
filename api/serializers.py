from api.models import TestCase
from rest_framework import serializers


class ApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ('id', 'name', 'module', 'method', 'uri', 'params', 'expect', 'create')
