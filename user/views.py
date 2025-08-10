from django.shortcuts import render

# Create your views here.
# views.py

from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import status, permissions, generics # Import generics
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import viewsets
from .models import SellerProfile # Import the new model
from .serializers import (SellerProfileSerializer,SellerRegistrationSerializer) # Import the new serializer
from .permissions import IsSellerProfileOwner
from rest_framework.views import APIView 




from user.models import Address, Profile
from user.permissions import IsUserAddressOwner, IsUserProfileOwner, IsSellerOrAdmin, IsBuyer # Import new permissions
from user.serializers import (
    AddressReadOnlySerializer,
  
    ProfileSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    ShippingAddressSerializer,
    BillingAddressSerializer,
    
)

User = get_user_model()


class UserRegisterationAPIView(RegisterView):
  
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response_data = {"detail": _("Verification e-mail sent.")}

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
    
class SellerRegisterationAPIView(APIView):
       
        serializer_class = SellerRegistrationSerializer
        permission_classes = [permissions.AllowAny] 

        def post(self, request, *args, **kwargs):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save() 

            
            return Response({
                "detail": _("Seller registration successful."),
                "user_id": user.id,
                "email": user.email,
            }, status=status.HTTP_201_CREATED)


class UserLoginAPIView(LoginView):
    

    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny] 


class UserProfileView(generics.RetrieveUpdateAPIView):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserProfileOwner] 

    def get_object(self):
        
        return self.request.user.profile


class AddressViewSet(viewsets.ModelViewSet):
    
    queryset = Address.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsUserAddressOwner] # Require authentication and ownership

    def get_serializer_class(self):
        if self.action == 'create':
            if 'address_type' in self.request.data:
                if self.request.data['address_type'] == Address.SHIPPING:
                    return ShippingAddressSerializer
                elif self.request.data['address_type'] == Address.BILLING:
                    return BillingAddressSerializer
        return AddressReadOnlySerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SellerProfileViewSet(viewsets.ModelViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
   

    def get_queryset(self):
        # For update/delete, we filter to ensure ownership
        if self.action in ['update', 'partial_update', 'destroy']:
             return self.queryset.filter(user=self.request.user)
        # For list and retrieve, we return the full queryset initially,
        # and permissions handle visibility.
        return self.queryset

    def get_permissions(self):
        if self.action in ['create']:
            # Allow any authenticated user to initiate seller profile creation (can be refined)
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['retrieve']:
            # Allow any authenticated user to view a single seller profile (can be AllowAny for public profiles)
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Only authenticated seller profile owners can update/delete their profile
            self.permission_classes = [permissions.IsAuthenticated, IsSellerProfileOwner]
        elif self.action in ['list']:
             # Only authenticated sellers or admins can list all seller profiles
             self.permission_classes = [permissions.IsAuthenticated, IsSellerOrAdmin]
        else:
            # Default permissions for other actions (if any)
            self.permission_classes = [permissions.IsAuthenticated]

        return super().get_permissions()

    def perform_create(self, serializer):
        
        serializer.save(user=self.request.user)