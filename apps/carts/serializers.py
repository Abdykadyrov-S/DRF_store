from rest_framework import serializers

from apps.products.serializers import ProductImageSerializer
from apps.products.models import Product
from apps.carts.models import Cart, CartItem

class CartProductSerializer(serializers.ModelSerializer):
    old_price = serializers.SerializerMethodField()

    class Meta:
        model = Product 
        fields = ('id', 'title', 'description', 'image', 'product_images', 'price', 'old_price', 
                  'currency', 'created',)

    def get_old_price(self, obj):
        if obj.price:
            return int(obj.price * 1.05)
        return None
    
class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity', 'is_selected')

class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity')

class CartSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField()
    cart_items = CartItemSerializer(many=True, read_only=True)

    def get_total_cost(self, obj):
        return obj.get_total_cost()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'cart_items', 'total_cost', 'created')