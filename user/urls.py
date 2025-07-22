# user/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter # Import DefaultRouter
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

from .views import (
    UserRegisterationAPIView,
    UserLoginAPIView, # Assuming you have a custom UserLoginAPIView
    UserProfileView,
    AddressViewSet, # Assuming you have AddressViewSet
    SellerRegisterationAPIView, # Import the new view
    SellerProfileViewSet, # Import the new viewset
)

# Create a router for ViewSets
router = DefaultRouter()
# Register AddressViewSet if you are managing addresses with a ViewSet
# router.register(r'addresses', AddressViewSet, basename='address')
router.register(r'seller-profiles', SellerProfileViewSet, basename='seller-profile')


urlpatterns = [
    # Include dj_rest_auth URLs (excluding those you override)
    # You might need to be careful here to avoid conflicts
    path('', include('dj_rest_auth.urls')),

    # Add path for user registration (using your custom view)
    path('registration/', UserRegisterationAPIView.as_view(), name='rest_register'),

    # If you have a custom login view, include it here
    # path('login/', UserLoginAPIView.as_view(), name='rest_login'),


    # Add path for user profile
    path('profile/', UserProfileView.as_view(), name='user_profile'),

    # Explicitly add password reset URLs if you are overriding them
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Seller registration
    path('seller/registration/', SellerRegisterationAPIView.as_view(), name='seller-registration'), # Added seller registration URL

    # ViewSet URLs (for seller profiles)
    # If you are using a ViewSet for addresses, uncomment the router.register line above
    path('', include(router.urls)), # Include router URLs for ViewSets
]
