from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
