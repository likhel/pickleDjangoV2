
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('product.urls')),
    path('api/auth/', include('user.urls')),
    path('api/', include('order.urls')),
    path('api/', include('wishlist.urls')),
   
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:  # only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)