from django.db import models
from django.conf import settings  # Import settings to get the AUTH_USER_MODEL
from user.models import CustomUser # Assuming your CustomUser is here
from PIL import Image

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    CATEGORY_TYPES = [
 ('ingredient', 'Ingredient Type'),
 ('flavor', 'Flavor Type'),
 ('style', 'Preparation Style'),
 ('packaging', 'Packaging Type'),
 ]
    slug = models.SlugField(unique=True)
    category_type = models.CharField(max_length=50, choices=CATEGORY_TYPES, default='ingredient' )

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"

class Product(models.Model):
    # Add a foreign key to the CustomUser model to represent the seller
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')

    categories = models.ManyToManyField(ProductCategory, related_name='products') # Changed from ForeignKey to ManyToManyField
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
        super().save(*args, **kwargs)  # Save the product first

        if self.image:
            img = Image.open(self.image.path)

            # Resize the image while maintaining aspect ratio
            max_size = (800, 800)  # Set your desired max size
            img.thumbnail(max_size, Image.LANCZOS)

            img.save(self.image.path)  # Save the resized image back