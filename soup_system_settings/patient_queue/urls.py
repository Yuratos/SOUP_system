from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('api/v1/patient-register/', views.RegisterPatientAPIView.as_view())
]
