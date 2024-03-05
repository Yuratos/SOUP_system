from django.shortcuts import render
from django.views import View

# Create your views here.


class AdminProfile(View): 
    
    def get(self, request): 
        return render(request, 'admin_lk/admin_lk.html')