from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from rest_framework.exceptions import NotAuthenticated

from apps.products.models import Product, ProductFavorite, ProductReview
from apps.products.serializers import ProductsSerializer, ProductFavoriteSerializer, \
    ProductReviewSerializer, ProductCreateReviewSerializer, ProductDetailSerializer, ProductFavoriteCreateSerializer
from apps.products.permissions import ProductPermission
from apps.products.pagination import ProductPagination
from apps.carts.models import Cart
from apps.products.filters import ProductFilter

# Create your views here.
class ProductsAPI(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'description', 'category', 'price', 'currency']
    search_fields = ['title', 'description', 'price', 'currency']
    ordering_fields = ['created', 'price', 'reviews__stars', 'created']  # Добавлено C  поле 'created' для сортировки
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        print(queryset.query)
        ordering = self.request.query_params.get('ordering', None)

        # Обработка сортировки по рейтингу
        if ordering == 'rating':
            queryset = queryset.annotate(avg_stars=models.Avg('reviews__stars')).order_by('-avg_stars')

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductsSerializer



class ProductFavoriteAPI(GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin):
    queryset = ProductFavorite.objects.all()
    serializer_class = ProductFavoriteSerializer

    def perform_create(self, serializer):
        # Проверка на аутентификацию теперь не требуется здесь, так как это будет обрабатываться через разрешения.
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ProductFavorite.objects.filter(user=self.request.user)
        else:
            raise NotAuthenticated('Вы должны войти в систему, чтобы выполнить это действие.')

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            # Для действий создания и удаления требуется, чтобы пользователь был аутентифицирован
            # и удовлетворял дополнительным критериям разрешений, определенным в ProductPermission.
            return (IsAuthenticated(), ProductPermission(),)
        # Для всех остальных действий доступ разрешен любому пользователю.
        return (AllowAny(),)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ProductFavoriteCreateSerializer
        return ProductFavoriteSerializer
    

class ReviewProductAPI(GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == "create":
            return ProductCreateReviewSerializer
        return ProductReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        avg_stars = queryset.aggregate(avg_stars=models.Avg('stars'))['avg_stars']
        return Response({'average_stars': avg_stars})

