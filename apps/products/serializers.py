from rest_framework import serializers
from urllib.parse import unquote

from apps.products.models import Product, ProductFavorite, ProductImage, ProductReview
from apps.users.serializers import UserSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ('id', 'product', 'image')

    def get_image(self, obj):
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url  # Вернуть относительный URL, если request не доступен или если изображение отсутствует

class ProductReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()  # Добавляем поле для имени пользователя
    class Meta:
        model = ProductReview
        fields = ('id', 'user', 'username', 'product', 'text', 
                  'stars', 'created_at')
        
    def get_username(self, obj):
        return obj.user.username

class ProductCreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ('id', 'user', 'product', 'text', 'stars')


class ProductsSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(read_only=True, many=True)
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    old_price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product 
        fields = ('id', 'title', 'description', 'image', 'product_images', 'price', 'old_price', 
                  'currency', 'review_count', 'average_rating', 'created',)

    def get_review_count(self, obj):
        return obj.get_review_count()

    def get_average_rating(self, obj):
        return obj.get_average_rating()
    
    def get_old_price(self, obj):
        return obj.old_price if obj.old_price else int(obj.price * 1.05)
        
    def get_image(self, obj):
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url  # Вернуть относительный URL, если request не доступен или если изображение отсутствует

class ProductDetailSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(read_only=True, many=True)
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    old_price = serializers.SerializerMethodField()
    product_reviews = ProductReviewSerializer(read_only=True, many=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product 
        fields = ('id', 'title', 'description', 'image', 'product_images', 'price', 'old_price', 
                  'currency', 'review_count', 'average_rating', 'product_reviews', 'created',)
        
 
    def get_review_count(self, obj):
        return obj.get_review_count()

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_old_price(self, obj):
        return obj.old_price if obj.old_price else int(obj.price * 1.05)
    
    def get_price(self, obj):
        return obj.price
    
    def get_image(self, obj):
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url  # Вернуть относительный URL, если request не доступен или если изображение отсутствует


class FavoriteProductsSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    old_price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    product_images = ProductImageSerializer(read_only=True, many=True)

    class Meta:
        model = Product 
        fields = ('id', 'title', 'description', 'image', 'product_images', 'price', 'old_price', 
                  'currency', 'review_count', 'average_rating', 'created',)
            
    def get_review_count(self, obj):
        return obj.get_review_count()

    def get_average_rating(self, obj):
        return obj.get_average_rating()
    
    def get_old_price(self, obj):
        return obj.old_price if obj.old_price else int(obj.price * 1.05)


class ProductFavoriteSerializer(serializers.ModelSerializer):
    product = FavoriteProductsSerializer(read_only=True)
    class Meta:
        model = ProductFavorite
        fields = ('id', 'product')

class ProductFavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFavorite
        fields = ('id', 'user', 'product')
