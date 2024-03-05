from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('doctor/', include('doctor.urls', namespace = 'doctor')), 
    path('place/', include('place.urls')), 
    path('patient_queue/', include('patient_queue.urls')),  
    path('admin_lk/', include('admin_lk.urls'))
]
