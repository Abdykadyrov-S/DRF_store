from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg

User = get_user_model()

# Create your models here
class Product(models.Model):
    CURRENCY_CHOICES = (
        ('KGS', 'KGS'),
        ('USD', 'USD'),
        ('EURO', 'EURO'),
        ('RUB', 'RUB'),
        ('KZT', 'KZT'),
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True, null=True
    )
    image = models.ImageField(
        max_length=1000,
        upload_to='product_images/',
        verbose_name="Фотография",
        default="product_images/no_image.png",
        blank=True, null=True
    )
    price = models.PositiveIntegerField(
        verbose_name="Цена",
        blank=True, null=True
    )
    old_price = models.PositiveIntegerField(
        verbose_name="Старая цена",
        blank=True, null=True
    )
    currency = models.CharField(
        max_length=100, verbose_name="Валюта",
        choices=CURRENCY_CHOICES,
        default="KGS"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return self.title

    def get_review_count(self):
        return self.product_reviews.count()

    def get_average_rating(self):
        average = self.product_reviews.aggregate(Avg('stars'))['stars__avg']
        return round(average, 2) if average else None
    
              
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="product_images",
        verbose_name="Продукт"
    )
    image = models.ImageField(
        upload_to="product_images/",
        verbose_name="Фотография"
    )

    def __str__(self):
        return f"{self.product}"
    
    class Meta:
        verbose_name = "Фотография продукта"
        verbose_name_plural = "Фотографии продуктов"

class ProductFavorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_favorites',
        verbose_name="Пользователь"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='product_favorites',
        verbose_name="Товар",
        unique=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
    
    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"


class ProductReview(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="user_reviews",
        verbose_name="Пользователь"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='product_reviews',
        verbose_name="Название продукта"
    )
    text = models.TextField(
        verbose_name="Текст для отзыва"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    stars = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name="Звезды", default=0
    )


    def __str__(self):
        return f"Отзыв от {self.user.username} для товара {self.product.title}"

    class Meta:
        verbose_name = "Отзыв товара"
        verbose_name_plural = "Отзывы товаров"