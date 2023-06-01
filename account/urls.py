from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update', views.profile_update, name='profile_update'),
    # path('profile/update', ProfileCreateUpdateView.as_view(), name='profile_update'),

]