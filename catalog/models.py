from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)


def save(self,*args,**kwargs):
    if not self.slug:
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)


def __str__(self):
    return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
name = models.CharField(max_length=120)
slug = models.SlugField(max_length=140, blank=True)


def save(self,*args,**kwargs):
    if not self.slug:
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)


def __str__(self):
    return f"{self.category.name} > {self.name}"


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['slug'])
        ]


def save(self,*args,**kwargs):
    if not self.slug:
        self.slug = slugify(self.title)[:255]
        super().save(*args,**kwargs)


def __str__(self):
    return self.title