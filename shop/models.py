from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from uuid import uuid4
from shop.validators import validate_file_size
from .managers import CustomUserManager

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    id = models.UUIDField(primary_key=True, default=uuid4, auto_created=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email


class Category(models.Model):
    CLOTHES = 'C'
    SHOES = 'S'
    HATS = 'H'
    CATEGORY_CHOICES = [
        (CLOTHES, 'Одежда'),
        (SHOES, "Обувь"),
        (HATS, "Головные уборы"),
    ]
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default=CLOTHES, unique=True)

    def __str__(self) -> str:
        return self.category


class Color(models.Model):
    BLACK = 'B'
    WHITE = 'W'
    RED = 'R'
    COLOR_CHOICES = [
        (BLACK, "Черный"),
        (WHITE, "Белый"),
        (RED, "Красный"),
    ]
    color = models.CharField(max_length=1, choices=COLOR_CHOICES, default=WHITE, unique=True)

    def __str__(self) -> str:
        return self.color


class Structure(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self) -> str:
        return self.name


class Size(models.Model):
    EXTRA_SMALL = 'XS'
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    UNDEFINED = 'ND'
    SIZE_CHOICES = [
        (EXTRA_SMALL, "XS"),
        (SMALL, "S"),
        (MEDIUM, "M"),
        (LARGE, "L"),
        (UNDEFINED, "ND"),
    ]
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default=MEDIUM, unique=True)

    def __str__(self) -> str:
        return self.size


class ShoppingCart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, auto_created=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(upload_to='shop/images', validators=[validate_file_size], blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=Category.CLOTHES)
    # color = models.ForeignKey(Color, on_delete=models.SET_DEFAULT, default=Color.WHITE)
    # size = models.ForeignKey(Size, on_delete=models.SET_DEFAULT, default=Size.MEDIUM)
    # category = models.ManyToManyField(Category)
    color = models.ManyToManyField(Color)
    size = models.ManyToManyField(Size, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    size = models.CharField(max_length=2)
    color = models.CharField(max_length=1)

    class Meta:
        unique_together = [['cart', 'product']]