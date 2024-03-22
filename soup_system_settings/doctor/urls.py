from django.urls import path
from . import views 

app_name = 'doctor'

urlpatterns = [
    path('doctor-page/', views.HelloDoctorPage.as_view(), name = 'doctor-page'), # Основная страница доктора
    path('api/v1/doctor-list/', views.GetDoctorsAPI.as_view()), # API - получение списка докторов
    path('api/v1/free-places/', views.GetFreePlacesAPI.as_view()), # API - получение списка свободных мест
    path('api/v1/all-places/', views.GetAllPlacesAPI.as_view()), # API - получение списка всех мест
    path('api/v1/add-remove-doctor', views.RemoveAddDoctorAPI.as_view()), # API - удаление или добавление доктора из коллектива
    path('api/v1/main-departaments', views.GetMainDepartaments.as_view()), # API - получение основных направлений
    path('api/v1/additional-departaments', views.GetAdditionalDepartaments.as_view()),
]
