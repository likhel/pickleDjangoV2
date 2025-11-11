from django.urls import path
from .views import WishlistListView, WishlistAddView, WishlistRemoveView

app_name = 'wishlist'

urlpatterns = [
    path('wishlist/', WishlistListView.as_view(), name='wishlist-list'),
    path('wishlist/add/', WishlistAddView.as_view(), name='wishlist-add'),
    path('wishlist/remove/<int:product_id>/', WishlistRemoveView.as_view(), name='wishlist-remove'),
]


