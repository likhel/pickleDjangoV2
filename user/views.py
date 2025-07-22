from django.shortcuts import render



from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import status, permissions, generics 
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import viewsets
from .models import SellerProfile
from .serializers import (SellerProfileSerializer,SellerRegistrationSerializer) 
from .permissions import IsSellerProfileOwner
from rest_framework.views import APIView 




from user.models import Address, Profile
from user.permissions import IsUserAddressOwner, IsUserProfileOwner, IsSellerOrAdmin, IsBuyer 
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
    permission_classes = [permissions.AllowAny]]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response_data = {"detail": _("Verification e-mail sent.")}

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
    
class SellerRegisterationAPIView(APIView):
        """
        Register new sellers and create their SellerProfile.
        """
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
    permission_classes = [permissions.IsAuthenticated, IsUserAddressOwner]
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
        
        if self.action in ['update', 'partial_update', 'destroy']:
             return self.queryset.filter(user=self.request.user)
        
        return self.queryset

    def get_permissions(self):
        if self.action in ['create']:
           
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['retrieve']:
            
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
           
            self.permission_classes = [permissions.IsAuthenticated, IsSellerProfileOwner]
        elif self.action in ['list']:
             self.permission_classes = [permissions.IsAuthenticated, IsSellerOrAdmin]
        else:
            self.permission_classes = [permissions.IsAuthenticated]

        return super().get_permissions()

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)
