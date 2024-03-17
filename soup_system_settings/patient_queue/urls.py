from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/patient-register/', views.RegisterPatientAPIView.as_view())
]
