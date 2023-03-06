from django.shortcuts import render


def home_p(request):
    return render(request, 'main/home.html')
