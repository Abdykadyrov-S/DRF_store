from django.db import models
from django.contrib.auth import get_user_model

from apps.products.models import Product

# Create your models here.
User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_carts", 
        verbose_name="Пользователь", unique=True
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания корзины"
    )

    def __str__(self):
        return f"{self.user}"
    
    def get_total_cost(self):
        total_cost = 0
        for item in self.cart_items.all():
            # Check if price and quantity are not None
            if item.product.price is not None and item.quantity is not None:
                total_cost += item.product.price * item.quantity
            else:
                # Log for debugging
                print(f"Warning: Null value encountered in cart item. Product price: {item.product.price}, Quantity: {item.quantity}")
        return total_cost
    
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items', 
        verbose_name="Корзина"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, 
        related_name='cart_items', verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        default=1, verbose_name="Количество товара"
    )
    is_selected = models.BooleanField(
        default=False, verbose_name='Выбран или нет'
    )

    def __str__(self):
        return f"{self.cart}"
    
    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
