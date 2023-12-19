from django.contrib.auth import views as auth_views
from django.urls import path
from .views import Home, Login, Logout


urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('home', Home.as_view(), name='home'),
]