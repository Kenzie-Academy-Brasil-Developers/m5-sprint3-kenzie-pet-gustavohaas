from rest_framework import serializers, status
from characteristics.models import Characteristic

class CharacteristicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length=20)
