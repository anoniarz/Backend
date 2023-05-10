from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='store-home'),
    path('products/<str:category>s/', views.products, name='store-products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-product/', views.add_product, name='add-product'),
    path('update-product/<int:pk>/', views.update_product, name='update-product')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)