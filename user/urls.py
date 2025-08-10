# user/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

from .views import (
    UserRegisterationAPIView,
    UserLoginAPIView, 
    UserProfileView,
    AddressViewSet,
    SellerRegisterationAPIView, 
    SellerProfileViewSet, 
)

router = DefaultRouter()

# router.register(r'addresses', AddressViewSet, basename='address')
router.register(r'seller-profiles', SellerProfileViewSet, basename='seller-profile')


urlpatterns = [
  
    path('', include('dj_rest_auth.urls')),

    
    path('registration/', UserRegisterationAPIView.as_view(), name='rest_register'),

 
    # path('login/', UserLoginAPIView.as_view(), name='rest_login'),


    
    path('profile/', UserProfileView.as_view(), name='user_profile'),

    
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    
    path('seller/registration/', SellerRegisterationAPIView.as_view(), name='seller-registration'), 

    
    
    path('', include(router.urls)), 
]
