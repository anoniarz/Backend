from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='ceneo_home'),
    path('products', views.products, name='products'),
    path('add_product', views.add_product, name='add_product'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(),
         name='product_reviews'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('products/refresh/<int:pk>/',
         views.refresh_product, name='refresh_product'),
    path('download-json/<int:pk>/',
         views.DownloadFile.as_view(), name='download_json'),
    path('favourites', views.favourites, name='favourites'),
    path('add-to-favourites/<int:pk>/',
         views.add_to_favourites, name='add_to_favourites'),
    path('remove-from-favourites/<int:pk>/',
         views.remove_from_favourites, name='remove_from_favourites'),
]
