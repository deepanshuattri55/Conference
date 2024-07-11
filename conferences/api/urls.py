from django.urls import path

from . import views

urlpatterns = [
    path('', views.ConferenceListView.as_view(), name='conference-list'),
    path('conf/<str:conf>/', views.ConferenceDetailView.as_view(), name='conference-detail'),
    path('conf/new/', views.ConferenceCreateView.as_view(), name='conference-create'),
]
