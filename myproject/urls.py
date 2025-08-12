

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('product.urls')),
    path('api/auth/', include('user.urls')),
    path('api/', include('order.urls')),
   
    path('accounts/', include('allauth.urls')),
]
