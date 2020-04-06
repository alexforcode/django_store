from django.db import models
from django.urls import reverse


class ProductManager(models.Manager):
    def all(self, *args, **kwargs):
        return super().get_queryset().filter(available=True)


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:category', kwargs={'category_slug': self.slug})


def get_image_path(instance, filename):
    filename = f'{instance.slug}.{filename.split(".")[1]}'
    return f'products/{instance.slug}/{filename}'


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    short_desc = models.TextField(blank=True)
    desc = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to=get_image_path, blank=True)
    available = models.BooleanField(default=True)
    objects = ProductManager()

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:product', kwargs={'product_slug': self.slug})
