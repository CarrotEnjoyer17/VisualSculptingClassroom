from django.contrib import admin
from django.urls import path, include

from users.views import login, registration, logout, profile
app_name = 'users'

urlpatterns = [
    path('login/', login, name = 'login'),
    path('registration/', registration, name = 'registration'),
    path('logout/', logout, name= 'logout'),
    path('profile/<int:user_id>/', profile, name='profile'),
]