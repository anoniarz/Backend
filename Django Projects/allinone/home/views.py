from django.shortcuts import render
from django.http import HttpResponse


def home_p(request):
    return render(request, 'home/home.html')
