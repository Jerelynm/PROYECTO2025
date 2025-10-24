from django.contrib import admin
from .models import Category, Brand, Product, ContactMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # autogenera slug desde nombre
    ordering = ('name',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'stock', 'is_active', 'created_at')
    list_filter = ('brand', 'category', 'is_active')
    search_fields = ('name', 'slug', 'brand__name', 'category__name')
    prepopulated_fields = {'slug': ('name',)}  # autogenera slug
    autocomplete_fields = ('brand', 'category')  # inputs con búsqueda
    ordering = ('name',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "created_at")
    search_fields = ("subject", "name", "email", "message")
    list_filter = ("created_at",)