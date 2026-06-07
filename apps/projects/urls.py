from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<slug:slug>/', views.project_detail, name='project_detail'),
    path('<slug:slug>/extra/', views.project_extra, name='project_extra'),
]