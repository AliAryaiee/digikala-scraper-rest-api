from itertools import product
from statistics import mode
from django.db import models


class Category(models.Model):
    """
        Category Model
    """
    title = models.CharField(max_length=256, unique=True)


class Product(models.Model):
    """
        Product Model
    """
    product_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=256)
    title_en = models.CharField(max_length=256, blank=True)
    price = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    link = models.CharField(max_length=512, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
