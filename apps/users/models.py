from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        blank=True, null=True
    )
    phone = models.CharField(
        max_length=50,
        verbose_name="Телефонный номер",
        blank=True, null=True,
        help_text="Телефонный номер"
    )
    profile_image = models.ImageField(
        upload_to='profiles_images/',
        verbose_name="Фотография профиля"
    )
    address = models.CharField(
        max_length=100,
        verbose_name="Адрес",
        blank=True, null=True,
        help_text="Адрес проживания"
    )
    
    def __str__(self):
        return self.username 

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
