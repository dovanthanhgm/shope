from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, CartItem, Category


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
        products = Product.objects.all()
        category_id = request.GET.get('category')
        if category_id:
            products = Product.objects.filter(category=Category.objects.get(id=category_id))
        return render(request, 'home.html', {
            'products': products,
            'categories': Category.objects.all()[:7],
        })

class AddToCart(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product_images = product.productimage_set.all()
        if product.has_variant():
            variants = product.variant_set.all()
            variant_images = []
            for variant in variants:
                variant_images.append(variant.image)

        return render(request, 'add_to_cart.html', {
            'product': product,
            'product_images': product_images,
            'variant_images': variant_images
        })
        user = self.request.user
        try:
            cart_item = CartItem.objects.get(user=user, product=product)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        except:
            CartItem.objects.create(user=user, product=product)
        return redirect(reverse('home'))
