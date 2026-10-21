from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('contact/', views.contact, name='contact'),
]