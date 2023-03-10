from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('products', views.products, name='products'),
    path('add_product', views.add_product, name='add_product'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(),
         name='product_reviews'),
]
