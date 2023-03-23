from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserRegisterForm
from .models import Profile
from django.core.paginator import Paginator
from main.views import Product


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def favourites(request):

    profile = request.user.profile
    favourites = profile.favourites.all()

    sorter = request.GET.get('sort')
    if sorter == 'a-z':
        favourites = favourites.order_by('product_name')
    elif sorter == 'z-a':
        favourites = favourites.order_by('-product_name')
    elif sorter == 'most_reviews':
        favourites = sorted(
            favourites, key=lambda p: p.reviews.count(), reverse=True)
    elif sorter == 'least_reviews':
        favourites = sorted(favourites, key=lambda p: p.reviews.count())
    elif sorter == 'highest_rating':
        favourites = favourites.order_by('-product_rating')
    elif sorter == 'lowest_rating':
        favourites = favourites.order_by('product_rating')
    elif sorter == 'highest_price':
        favourites = favourites.order_by('-product_price')
    elif sorter == 'lowest_price':
        favourites = favourites.order_by('product_price')

    paginator = Paginator(favourites, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'favourites': page_obj,
        "sorter": sorter,
    }

    return render(request, 'users/favourites.html', context)


@login_required
def add_to_favourites(request, pk):
    product = Product.objects.get(product_id=pk)
    profile = request.user.profile
    profile.add_to_favourites(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_from_favourites(request, pk):
    product = get_object_or_404(Product, product_id=pk)
    profile = get_object_or_404(Profile, user=request.user)
    profile.favourites.remove(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('login')
