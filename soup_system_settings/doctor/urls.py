from django.contrib import admin
from django.urls import include, path
from . import views 

app_name = 'doctor'

urlpatterns = [
    path('doctor-page/', views.HelloDoctorPage.as_view(), name = 'doctor-page'),
    path('api/v1/doctor-list/', views.GetDoctorsAPI.as_view()), 
    path('api/v1/free-places/', views.GetFreePlacesAPI.as_view()), 
    path('api/v1/add-remove-doctor', views.RemoveAddDoctorAPI.as_view()) 
]
