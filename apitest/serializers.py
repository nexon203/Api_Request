from rest_framework import serializers
from apitest.models import TestModel


class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ['name', 'address', 'number', 'age']
        
