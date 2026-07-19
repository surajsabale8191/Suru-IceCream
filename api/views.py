from django.shortcuts import render
from Home.models import Contact
from .serializers import ContactSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view



# Create your views here.
@api_view(['Post'])
def contactView(requset):
    if requset.method=="POST":
        serializer=ContactSerializer(data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

        