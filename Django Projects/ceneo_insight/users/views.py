from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserRegisterForm
from .models import Profile
from main.views import Product


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def favourites(request):

    sort_by = request.GET.get('sort_by')
    profile = request.user.profile
    favourites = profile.favourites.all()

    if sort_by == 'a-z':
        favourites = favourites.order_by('product_name')
    elif sort_by == 'z-a':
        favourites = favourites.order_by('-product_name')
    elif sort_by == 'most_reviews':
        favourites = sorted(
            favourites, key=lambda p: p.reviews.count(), reverse=True)
    elif sort_by == 'least_reviews':
        favourites = sorted(favourites, key=lambda p: p.reviews.count())
    elif sort_by == 'highest_rating':
        favourites = favourites.order_by('-product_rating')
    elif sort_by == 'lowest_rating':
        favourites = favourites.order_by('product_rating')
    request.session['sort_by'] = sort_by

    context = {
        'favourites': favourites,
        "sort_by": sort_by,
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
