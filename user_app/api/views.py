from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.shortcuts import render
from django.views.generic import TemplateView
import logging
from user_app.api import serializers
from user_app import models

logger = logging.getLogger(__name__)
class UserRegisterView(generics.CreateAPIView):
    serializer_class = serializers.CustomUserSerializer

    def get(self, request):
        return render(request, 'html/signup.html')

    def post(self, request, *args, **kwargs):
        logger.info("Received registration POST request")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            logger.info("Serializer valid")
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            logger.error("Serializer errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    serializer_class = serializers.UserLoginSerializer

    def get(self, request):
        return render(request, 'html/login.html')

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, username=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "User successfully logged out."}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def get_view_name(self):
        return "Account Info"

# New views for rendering HTML templates
class IndexView(TemplateView):
    template_name = "html/index.html"

class ContactUsView(TemplateView):
    template_name = "html/contactUs.html"

class ConferenceCreateView(TemplateView):
    template_name = "html/conference_create.html"

class LearnMoreView(TemplateView):
    template_name = "html/learnmore.html"

class AuthorsNewSubmissionView(TemplateView):
    template_name = "html/Authors_new_submission.html"
