from django.db import models
from django.conf import settings  
from user.models import CustomUser 
from PIL import Image

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
  
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    ingredients = models.TextField(help_text="List the ingredients of the product")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    expiration_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  

        if self.image:
            img = Image.open(self.image.path)

            
            max_size = (800, 800) 
            img.thumbnail(max_size, Image.LANCZOS)

            img.save(self.image.path)  
