from django.urls import path

from linkers.api import views

urlpatterns = [
    path('editor/conferences/', views.EditorConferenceListView.as_view(), name='editor-dashboard'),
    path('editors/conf/<str:conf>/add/', views.EditorConferenceCreateView.as_view(), name='editor-add'),
    path('reviewer/conferences/', views.ReviewerConferenceListView.as_view(), name='reviewer-dashboard'),
    path('reviewer/conf/<str:conf>/add/', views.ReviewerConferenceCreateView.as_view(), name='reviewer-add'),
    path('reviewer/conf/<str:conf>/papers/', views.ReviewerPaperListView.as_view(), name='reviewer-papers'),
    path('reviewer/conf/<str:conf>/paper/<int:pk>/add/', views.ReviewerPaperCreateView.as_view(), name='reviewer-add'),
]
