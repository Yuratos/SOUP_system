from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('place-controller/<str:place_name>/<str:doctor_info>', views.PlaceController.as_view()), 
    path('place-screen/<str:place_number>', views.PlaceScreen.as_view()), 
]
