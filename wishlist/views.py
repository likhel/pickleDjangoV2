from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Wishlist
from .serializers import WishlistSerializer, WishlistAddSerializer
from product.models import Product


class WishlistListView(APIView):
    """
    GET /api/wishlist - Get all wishlist items for the logged-in user
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist_items, many=True)
        return Response({
            'count': wishlist_items.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)


class WishlistAddView(APIView):
    """
    POST /api/wishlist/add - Add a product to the wishlist
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WishlistAddSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            product = get_object_or_404(Product, id=product_id)
            
            # Check if item already exists in wishlist
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=request.user,
                product=product
            )
            
            if created:
                response_serializer = WishlistSerializer(wishlist_item)
                return Response({
                    'message': 'Product added to wishlist successfully.',
                    'data': response_serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                response_serializer = WishlistSerializer(wishlist_item)
                return Response({
                    'message': 'Product is already in your wishlist.',
                    'data': response_serializer.data
                }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishlistRemoveView(APIView):
    """
    DELETE /api/wishlist/remove/:productId - Remove a product from the wishlist
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, product_id):
        try:
            wishlist_item = Wishlist.objects.get(
                user=request.user,
                product_id=product_id
            )
            product_name = wishlist_item.product.name
            wishlist_item.delete()
            return Response({
                'message': f'Product "{product_name}" removed from wishlist successfully.'
            }, status=status.HTTP_200_OK)
        except Wishlist.DoesNotExist:
            return Response({
                'error': 'Product not found in your wishlist.'
            }, status=status.HTTP_404_NOT_FOUND)
