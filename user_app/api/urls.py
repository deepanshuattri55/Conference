from django.urls import path, include

from . import views

urlpatterns = [
    path('info/', views.UserDetailView.as_view(), name='account-info'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('', views.IndexView.as_view(), name='index'),
]
