# Generated by Django 5.0 on 2024-03-27 13:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carts', '0001_initial'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_carts', to=settings.AUTH_USER_MODEL, unique=True, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='carts.cart', verbose_name='Корзина'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='products.product', verbose_name='Товар'),
        ),
    ]
