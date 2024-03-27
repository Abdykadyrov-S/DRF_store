from django.db import models
from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget

from apps.products.models import Product, ProductImage, ProductFavorite, ProductReview

# Register your models here.
class ImageTabularInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'created')
    search_fields = ('title', 'created')
    list_per_page = 20
    inlines = [ImageTabularInline]

@admin.register(ProductFavorite)
class ProductFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__username', 'product__title')

@admin.register(ProductReview)
class StarsProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'stars')
    search_fields = ('user__username', 'product__title')
