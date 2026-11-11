from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('start-unraid/', views.start_unraid, name='start_unraid'),
]
