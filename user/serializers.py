from dj_rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers
from .models import SellerProfile
from phonenumber_field.serializerfields import PhoneNumberField
from django_countries.serializers import CountryFieldMixin
from django_countries.serializer_fields import CountryField  
from django.db import transaction

from .exceptions import (
    AccountDisabledException,
    AccountNotRegisteredException,
    InvalidCredentialsException,
)
from .models import Address, Profile

User = get_user_model()


class UserRegistrationSerializer(RegisterSerializer):
  

    username = None
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=False,allow_blank=True, write_only=True)

    def validate(self, validated_data):
        email = validated_data.get("email", None)
        phone_number = validated_data.get("phone_number", None)

        if not (email or phone_number):
            raise serializers.ValidationError(_("Enter an email or a phone number."))

        if validated_data["password1"] != validated_data["password2"]:
            raise serializers.ValidationError(_("The two password fields didn't match."))

        return validated_data

    def get_cleaned_data_extra(self):
        return {
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "phone_number": self.validated_data.get("phone_number", ""),
        }

    def create_extra(self, user, validated_data):
        user.first_name = validated_data.get("first_name")
        user.last_name = validated_data.get("last_name")
        user.save()

        # Save phone number to Profile model
        phone_number = validated_data.get("phone_number")
        if phone_number == "":
           phone_number = None
        if phone_number is not None:
            Profile.objects.update_or_create(user=user, defaults={"phone_number": phone_number})

    def custom_signup(self, request, user):
        self.create_extra(user, self.get_cleaned_data_extra())


class SellerProfileSerializer(serializers.ModelSerializer):
    """
    
    Used for nested serialization in seller registration and for managing seller profiles.
    """
    
    business_phone_number = PhoneNumberField(required=False, allow_null=True)
    business_country = CountryField(required=False, allow_null=True)

    class Meta:
        model = SellerProfile
        
        fields = [
            'business_name',
            'business_type',
            'business_registration_number',
            'tax_identification_number',
            'bank_name',
            'bank_account_number',
            'bank_account_holder_name',
            'business_phone_number',
            'business_email',
            'business_country',
            'business_city',
            'business_street',
            'business_postal_code',
            'shipping_policy',
            'return_policy',
            'is_verified', 
        ]
        read_only_fields = ['is_verified']


class SellerRegistrationSerializer(serializers.Serializer):
    
   
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    
    seller_profile = SellerProfileSerializer()

    def validate_email(self, value):
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("User with this email already exists."))
        return value

    def create(self, validated_data):
        with transaction.atomic(): 
            seller_profile_data = validated_data.pop('seller_profile')

            # Create the user with 'seller' role
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                role='seller' 
            )

            
            SellerProfile.objects.create(user=user, **seller_profile_data)

        return user 

    #  add an update method if you allow users to transition from buyer to seller
    # def update(self, instance, validated_data):
    #     # Handle updating user and creating/updating seller profile
    #     pass


class UserLoginSerializer(serializers.Serializer):
   
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})



    def validate(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")

        if email and password:
            
            user = authenticate(username=email, password=password)
        else:
            raise serializers.ValidationError(
                _("Enter an email and password.")
            )

        if not user:
            raise InvalidCredentialsException()

        if not user.is_active:
            raise AccountDisabledException()

        validated_data["user"] = user
        return validated_data
class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = (
            "avatar",
            "bio",
            "phone_number",  
            "created_at",
            "updated_at",
        )


class AddressReadOnlySerializer(CountryFieldMixin, serializers.ModelSerializer):
   
    user = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = Address
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
   

    profile = ProfileSerializer(read_only=True)
    addresses = AddressReadOnlySerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "profile",
            "addresses",
        )


class ShippingAddressSerializer(CountryFieldMixin, serializers.ModelSerializer):
   

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ("address_type",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["address_type"] = "S"
        return representation

    def validate(self, data):
        if not data.get('city'):
            raise serializers.ValidationError({"city": _("City is required.")})
        if not data.get('street'):
            raise serializers.ValidationError({"street": _("Street is required.")})
        if not data.get('country'):
            raise serializers.ValidationError({"country": _("Country is required.")})
        return data


class BillingAddressSerializer(CountryFieldMixin, serializers.ModelSerializer):
    
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ("address_type",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["address_type"] = "B"
        return representation

    def validate(self, data):
        if not data.get('city'):
            raise serializers.ValidationError({"city": _("City is required.")})
        if not data.get('street'):
            raise serializers.ValidationError({"street": _("Street is required.")})
        if not data.get('country'):
            raise serializers.ValidationError({"country": _("Country is required.")})
        return data
    

