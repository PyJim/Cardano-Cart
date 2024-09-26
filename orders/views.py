from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied

from cart.models import Cart
from .models import Order
from .serializers import OrderSerializer


class OrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Retrieve the cart for the current user
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            raise NotFound("Cart not found for the user.")

        # Ensure the cart has items
        if not cart.items.exists():
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare the data for the order
        order_data = {
            'shipping_address': request.data.get('shipping_address'),
            'tracking_number': request.data.get('tracking_number', ''),
        }

        # Pass the cart in the context to the serializer
        serializer = self.get_serializer(data=order_data, context={'cart': cart, 'request': request})

        if serializer.is_valid():
            order = serializer.save()

            # Optionally clear the cart after order creation
            cart.items.all().delete()

            return Response({
                "message": "Order created successfully",
                "order": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request, order_id=None):
        if request.user.role == 'admin':
            if order_id:
                # Get the order by ID
                try:
                    order = Order.objects.get(id=order_id)
                except Order.DoesNotExist:
                    raise NotFound(detail="Order not found.")
                
                serializer = self.get_serializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            orders = Order.objects.all()
            serializer = self.get_serializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif order_id is not None:
            # Retrieve product by ID or return 404 if not found
            try:
                order = Order.objects.get(id=order_id, buyer=request.user)
            except Order.DoesNotExist:
                return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        
            order = get_object_or_404(Order, id=order_id, buyer=request.user)
            serializer = self.get_serializer(order)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        order = Order.objects.all()
        orders = Order.objects.filter(buyer=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, order_id=None):
        if order_id is not None:
            # Retrieve product by ID or return 404 if not found
            try:
                order = Order.objects.get(id=order_id, buyer=request.user)
            except Order.DoesNotExist:
                return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
            order = get_object_or_404(Order, id=order_id, buyer=request.user)

            # Ensure the requesting user is deleting their own order or has admin permissions
            if request.user != order.buyer and not request.user.is_superuser:
                return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        
            order.delete()
            return Response({
                "message": "Order deleted successfully."
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, order_id=None):
        if order_id is not None:
            # Retrieve order by ID or return 404 if not found
            try:
                order = Order.objects.get(id=order_id, buyer=request.user)
            except Order.DoesNotExist:
                return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
            
            # Ensure the requesting user is updating their own order or has admin permissions
            if request.user != order.buyer and not request.user.is_superuser:
                return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
            
            order = get_object_or_404(Order, id=order_id, buyer=request.user)
            serializer = OrderSerializer(order, data=request.data, context={'request': request}, partial=False)  # full update (PUT)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Order updated successfully",
                    "order": serializer.data
                }, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)