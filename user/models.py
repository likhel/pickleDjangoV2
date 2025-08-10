# user/models.py

import datetime
import requests

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

from django.utils import timezone
from rest_framework.exceptions import NotAcceptable
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField 



class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='buyer')
    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username']

    class Meta:
        swappable = 'AUTH_USER_MODEL'

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar', blank=True)
    bio = models.CharField(max_length=200, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True) # Added phone_number field

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.get_full_name()


class Address(models.Model):
    BILLING = "B"
    SHIPPING = "S"

    ADDRESS_CHOICES = ((BILLING, _("billing")), (SHIPPING, _("shipping")))

    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    country = CountryField()
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    apartment = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()


class SellerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="seller_profile", on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=100, blank=True)
    business_registration_number = models.CharField(max_length=100, blank=True, null=True) # Optional
    tax_identification_number = models.CharField(max_length=100, blank=True)

  
    bank_name = models.CharField(max_length=255, blank=True)
    bank_account_number = models.CharField(max_length=255, blank=True)
    bank_account_holder_name = models.CharField(max_length=255, blank=True)

    
    business_phone_number = PhoneNumberField(blank=True, null=True)
    business_email = models.EmailField(max_length=255, blank=True)
    business_country = CountryField(blank=True, null=True)
    business_city = models.CharField(max_length=100, blank=True)
    business_street = models.CharField(max_length=255, blank=True)
    business_postal_code = models.CharField(max_length=20, blank=True)

    
    shipping_policy = models.TextField(blank=True)
    return_policy = models.TextField(blank=True)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name or self.user.get_full_name()






     


