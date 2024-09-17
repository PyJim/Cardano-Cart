# cart/views.py
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartItemSerializer

class CartProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Validate and parse request data
        serializer = CartItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']

            # Retrieve or create the cart for the user
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Check if the item already exists in the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                # If item already exists, update the quantity
                cart_item.quantity += quantity
                cart_item.save()
            else:
                # If item is new, set the quantity
                cart_item.quantity = quantity
                cart_item.save()

            # Update cart total price
            cart.total_price = sum(item.get_total_item_price() for item in cart.items.all())
            cart.save()

            return Response({"message": "Item added to cart successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, product_id=None):
        # Retrieve the user's cart
        cart = get_object_or_404(Cart, user=request.user)

        if product_id:
            # If product_id is provided, remove that specific product
            cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
            cart_item.delete()
        else:
            # If no product_id is provided, remove all products from the cart
            cart.items.all().delete()

        # Update the cart's total price
        cart.total_price = sum(item.get_total_item_price() for item in cart.items.all())
        cart.save()

        return Response({"message": "Cart updated successfully"}, status=status.HTTP_200_OK)
    

    def put(self, request, product_id=None):
        # Validate and parse request data
        if product_id is not None:
            serializer = CartItemSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                quantity = serializer.validated_data['quantity']

                # Retrieve the user's cart
                cart = get_object_or_404(Cart, user=request.user)

                # Retrieve and update the CartItem
                cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
                cart_item.quantity = quantity
                cart_item.save()

                # Update the cart's total price
                cart.total_price = sum(item.get_total_item_price() for item in cart.items.all())
                cart.save()

                # Prepare the response data
                response_data = {
                    "message": "Item updated in cart successfully",
                    "item": {
                        "product_id": cart_item.product.id,
                        "quantity": cart_item.quantity
                    }
                }

                return Response(response_data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    
    def get(self, request):
        # Retrieve the user's cart
        cart = get_object_or_404(Cart, user=request.user)

        # Prepare the response data
        cart_items = CartItem.objects.filter(cart=cart)
        items_data = [
            {
                "product_id": item.product.id,
                "quantity": item.quantity
            }
            for item in cart_items
        ]
        
        response_data = {
            "items": items_data,
            "total_price": cart.total_price
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    


