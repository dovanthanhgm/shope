from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, CartItem


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

class AddToCart(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        user = self.request.user
        try:
            cart_item = CartItem.objects.get(user=user, product=product)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        except:
            CartItem.objects.create(user=user, product=product)
        return redirect(reverse('home'))
