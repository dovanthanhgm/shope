from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(auth.models.AbstractBaseUser, auth.models.PermissionsMixin):
    username = models.CharField(_("username"), max_length=100, unique=True, validators=[auth.validators.UnicodeUsernameValidator()], error_messages={"unique": _("A user with that username already exists."),})
    first_name = models.CharField(_("first name"), max_length=100, blank=True)
    last_name = models.CharField(_("last name"), max_length=100, blank=True)    # Surname
    email = models.EmailField(_("email address"), blank=True)
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_seller = models.BooleanField(default=False, null=True, blank=True)
    is_staff = models.BooleanField(_("staff status"), default=False,)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = auth.models.UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
    
    def cart_count(self):
        return self.cartitem_set.count()

    def __str__(self):
        identifier = self.username
        try:
            if self.last_name != "" or self.first_name != "":
                identifier = f"{self.last_name} {self.first_name}"
        except:
            pass
        return identifier

class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='category', null=True, blank=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=54, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def has_variant(self):
        print(self.variant_set.count())
        return self.variant_set.count() > 0
    def image(self):
        products = ProductImage.objects.all()
        return products[0].file.url
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    file = models.ImageField(upload_to='product_image', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='variant_image', null=True, blank=True)
    attribute_name = models.CharField(max_length=100, null=True, blank=True)
    attribute_value = models.CharField(max_length=100, null=True, blank=True)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
