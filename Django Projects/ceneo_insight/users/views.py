from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
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
    products = Product.objects.all()
    
    if sort_by == 'a-z':
        products = products.order_by('product_name')
    elif sort_by == 'z-a':
        products = products.order_by('-product_name')
    elif sort_by == 'most_reviews':
        products = sorted(products, key=lambda p: p.reviews.count(), reverse=True)
    elif sort_by == 'least_reviews':
        products = sorted(products, key=lambda p: p.reviews.count())
    elif sort_by == 'highest_rating':
        products = products.order_by('-rating')
    elif sort_by == 'lowest_rating':
        products = products.order_by('rating')
        
    request.session['sort_by'] = sort_by
    
    context = {
        'favourites': favourites,
        'produxts': products,
        "sort_by": sort_by,
    }
    
    return render(request, 'users/favourites.html', context)

def add_to_favourites(request, pk):
    product = Product.objects.get(product_id=pk)
    
    profile = request.user.profile
    profile.add_to_favourites(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_favourites(request, pk):
    product = get_object_or_404(Product, product_id=pk)
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        profile.favourites.remove(product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))