from django.urls import path

from reviews.api import views

urlpatterns = [
    path('conf/<str:conf>/paper/<int:pk>/', views.ReviewListView.as_view(), name='reviews-list'),
    path('conf/<str:conf>/paper/<int:pk>/review/<int:review_pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('conf/<str:conf>/paper/<int:pk>/review/create/', views.ReviewCreateView.as_view(), name='review-create')
]