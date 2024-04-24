from django.urls import path
from . import views


urlpatterns = [
    path('', views.AdminProfile.as_view()), # Маршрут кабинета администратора
]
