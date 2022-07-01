from rest_framework import serializers, status
from groups.serializer import GroupSerializer
from characteristics.serializer import CharacteristicSerializer
from groups.models import Group
from characteristics.models import Characteristic
from animals.models import Animal

class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length=50)
    age = serializers.FloatField()
    weight = serializers.FloatField()
    sex = serializers.CharField(max_length=15)
    group = GroupSerializer()
    characteristics = CharacteristicSerializer(many=True)


    def create(self, validated_data: dict):
        obrigatory_keys = {"name", "age", "weight", "sex", "group", "characteristics"}
        missing_keys = []

        for key, value in validated_data.items():
            if key not in obrigatory_keys:
                error = {key: ["This field is required."]}
                missing_keys.push(error)    

        if missing_keys:
            raise KeyError({ missing_keys }, status.HTTP_400_BAD_REQUEST)

        group_data = validated_data.pop("group")
        characteristics_data = validated_data.pop("characteristics")

        group, _ = Group.objects.get_or_create(**group_data)

        animal = Animal.objects.create(**validated_data, group=group)
        
        for characteristic in characteristics_data:
            characteristic, _ = Characteristic.objects.get_or_create(**characteristic)
            print(characteristic)
            animal.characteristics.add(characteristic)        

        return animal

    def update(self, instace: Animal, validated_data: dict):
        non_updatable = {"sex", "group"}

        for key, value in validated_data.items():
            if key in non_updatable:
                raise KeyError(
                    { "message": f"You can not update {key} property."},
                    status.HTTP_400_BAD_REQUEST,        
                )
            setattr(instace, key, value)
            instace.save()

        return instace

