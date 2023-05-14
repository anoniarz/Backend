from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Product
from .forms import ProductForm
from django.views.generic import DetailView

# Create your views here.

def home(request):

    categories = Product.objects.values_list('category', flat=True).distinct()

    context = {
        'categories': categories,

    }

    return render(request, 'store/home.html', context)


def products(request, category):

    if category:
        products = Product.objects.all().filter(category=category)

    context = {
        'products': products,
    }

    return render(request, 'store/products.html', context)

class ProductDetailView(DetailView):
    model = Product



@user_passes_test(lambda u: u.is_staff)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store-home')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product-detail', pk=product.pk)
    return render(request, 'store/update_product.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def delete_product(request, pk):
    Product.objects.filter(pk=pk).delete()
    page = request.META.get('HTTP_REFERER')
    return redirect(page)