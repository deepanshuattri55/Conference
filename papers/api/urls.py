from django.urls import path

from papers.api import views

urlpatterns = [
    path('user/', views.PaperListView.as_view(), name='paper-list'),
    path('user/paper/<int:pk>/', views.PaperDetailView.as_view(), name='paper-detail'),
    path('conf/<str:conf>/paper/new/', views.PaperCreateView.as_view(), name='paper-create')
]
