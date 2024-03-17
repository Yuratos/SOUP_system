from django.urls import include, path
from . import views 

app_name = 'doctor'

urlpatterns = [
    path('doctor-page/', views.HelloDoctorPage.as_view(), name = 'doctor-page'), # Основная страница доктора
    path('api/v1/doctor-list/', views.GetDoctorsAPI.as_view()), # API - получение списка докторов
    path('api/v1/free-places/', views.GetFreePlacesAPI.as_view()), # API - получение списка свободных мест
    path('api/v1/all-places/', views.GetAllPlacesAPI.as_view()), # API - получение списка всех мест
    path('api/v1/add-remove-doctor', views.RemoveAddDoctorAPI.as_view()) # API - удаление или добавление доктора из коллектива
]
