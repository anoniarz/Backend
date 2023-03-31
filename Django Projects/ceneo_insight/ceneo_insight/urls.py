from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('register/', user_views.register, name='register'),
    path('favourites/', user_views.favourites, name='favourites'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('add-to-favourites/<int:pk>/',
         user_views.add_to_favourites, name='add_to_favourites'),
    path('remove-from-favourites/<int:pk>/',
         user_views.remove_from_favourites, name='remove_from_favourites'),
]
