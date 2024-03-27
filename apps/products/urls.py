from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.products import views

router = DefaultRouter()
router.register('products', views.ProductsAPI, 'api_products')
router.register('favorite', views.ProductFavoriteAPI, 'api_favorite')
router.register('review', views.ReviewProductAPI, 'api_review')

urlpatterns = [

]

urlpatterns += router.urls