# store/admin.py
from django.contrib import admin
from .models import Product, Category, ContactMessage, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",           # <- existe porque lo hicimos FK
        "price",
        "display_discount_price",
        "display_on_sale",
        "is_active",
        "created_at",
    )
    list_filter = ("category", "is_active", "created_at")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)

    # helpers seguros para columnas calculadas
    def display_discount_price(self, obj):
        return getattr(obj, "discount_price", None) or "—"
    display_discount_price.short_description = "discount_price"

    def display_on_sale(self, obj):
        dp = getattr(obj, "discount_price", None)
        price = getattr(obj, "price", None)
        try:
            return bool(dp is not None and price is not None and dp < price)
        except Exception:
            return False
    display_on_sale.boolean = True
    display_on_sale.short_description = "on_sale"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    ordering = ("name",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "created_at")
    search_fields = ("subject", "name", "email", "message")
    list_filter = ("created_at",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'customer_name', 'total')
    readonly_fields = ('created_at',)