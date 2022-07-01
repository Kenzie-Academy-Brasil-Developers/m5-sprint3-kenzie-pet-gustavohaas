from functools import partial
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status

from animals.models import Animal
from animals.serializer import AnimalSerializer

class AnimalView(APIView):
    def get(self, _: Request):
        
        animals = Animal.objects.all()
        serialized = AnimalSerializer(instance=animals, many=True)

        return Response({"animals": serialized.data}, status.HTTP_200_OK)
        
        
    def post(self, request: Request):
        try:
            serialized = AnimalSerializer(data=request.data)
            serialized.is_valid(raise_exception=True)
            serialized.save()

            return Response(serialized.data, status.HTTP_201_CREATED)

        except KeyError as err:
            return Response(*err.args)

class AnimalIdView(APIView):
    def get(self, _: Request, animal_id: int):
        try:
            animal = get_object_or_404(Animal, pk=animal_id)

            serialized = AnimalSerializer(animal)

            return Response(serialized.data, status.HTTP_200_OK)
        
        except Http404:
            return Response({"message": "Animal not found."}, status.HTTP_404_NOT_FOUND)

    def patch(self, request:Request, animal_id: int):
        try:
            animal = get_object_or_404(Animal, pk=animal_id)

            serialized = AnimalSerializer(animal, request.data, partial=True)
            serialized.is_valid(raise_exception=True)
            serialized.save()

            return Response(serialized.data, status.HTTP_200_OK)

        except Http404:
            return Response({"message": "Animal not found."}, status.HTTP_404_NOT_FOUND)

        except KeyError as err:
            return Response(*err.args)
    

    def delete(self, _: Request, animal_id: int):
        try:
            animal = get_object_or_404(Animal, pk=animal_id)

            animal.delete()

            return Response({}, status.HTTP_200_OK)

        except Http404:
            return Response({"message": "Animal not found."}, status.HTTP_404_NOT_FOUND)