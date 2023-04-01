from django.shortcuts import render


def home(request):

    username = 'Anon'
    if request.user.is_authenticated:
        profile = request.user.profile
        username = profile.user

    return render(request, 'home/home.html', {'username': username})
