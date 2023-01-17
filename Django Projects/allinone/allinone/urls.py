
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    
    path('mockaroo/', include('mockaroo.urls')),
    path('admin/', admin.site.urls),
    
]