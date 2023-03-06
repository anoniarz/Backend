from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_p, name='home'),
]
