from django.shortcuts import render
from django.http import HttpResponse


def mock(request):
    return render(request, 'main.html')
