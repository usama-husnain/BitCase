from django.urls import path, include
from . import views

urlpatterns = [
    path('users/', views.index, name='users')
]