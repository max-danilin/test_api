from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models

# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # list_display = ['name', 'image', 'get_category', 'size', 'color', 'price']
    list_display = ['name', 'image', 'price']
    # list_editable = ['size', 'color']
    ordering = ['name']
    list_per_page = 10
    # list_select_related = ['category', 'size', 'color']

    # def get_category(self, obj):
    #     return [str(category) for category in obj.category.all()]

    # def category_title(self, product):
    #     return product.category.category

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']
    # list_editable = ['category']


@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['color']
    # list_editable = ['color']


@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']
    # list_editable = ['size']