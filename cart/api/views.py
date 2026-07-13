from rest_framework import generics, permissions
from cart.models import Cart
from .serializers import CartSerializer


class CartDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Cart.objects.filter(user=self.request.user, is_active=True).first()
