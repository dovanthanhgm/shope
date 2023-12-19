from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return render(request, 'login.html')
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error_message': 'Thông tin đăng nhập không đúng.'})
    
class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        next_url = request.GET.get('next', '/')
        return redirect(next_url)

class Home(View):
    def get(self, request):
        return render(request, 'home.html', {
            'products': Product.objects.all(),
            
        })


