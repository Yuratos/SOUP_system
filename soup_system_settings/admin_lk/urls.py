from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.AdminProfile.as_view()), 
]
