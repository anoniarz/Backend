from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='ceneo-home'),
    path('products', views.products, name='products'),
    path('add_product', views.add_product, name='add-product'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(),
         name='product-reviews'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete-product'),
    path('products/refresh/<int:pk>/',
         views.refresh_product, name='refresh-product'),
    path('download-json/<int:pk>/',
         views.DownloadFile.as_view(), name='download-json'),
    path('favourites', views.favourites, name='favourites'),
    path('add-to-favourites/<int:pk>/',
         views.add_to_favourites, name='add-to-favourites'),
    path('remove-from-favourites/<int:pk>/',
         views.remove_from_favourites, name='remove-from-favourites'),
]
