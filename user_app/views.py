from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def login_user(request):
    # Handle login logic
    return Response({"message": "User logged in"})