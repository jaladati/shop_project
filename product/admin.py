from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['title', 'is_enable']
    readonly_fields = ['slug']
    list_editable = ['is_enable']
    list_filter = ['is_enable', 'parent']
    search_fields = ['title']


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery


class ProductColorVariantInline(admin.TabularInline):
    model = ProductColorVariant


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['short_title', 'price', 'off', 'stock_count', 'is_enable']
    readonly_fields = ['created_time', 'updated_time', 'stock_count']
    list_editable = ['price', 'off', 'is_enable']
    date_hierarchy = "created_time"
    search_fields = ['title', 'short_description', 'description']
    list_filter = ['category']
    raw_id_fields = ['category']
    inlines = [
        ProductGalleryInline,
        ProductColorVariantInline,
    ]

    def short_title(self, obj):
        return F"{obj.title[:15]}..."


@admin.register(ProductColorVariant)
class ProductColorVariantAdmin(admin.ModelAdmin):
    list_display = ("short_product_name", "price", "off", "color_name", "stock_count")
    list_editable = ("price", "off", "stock_count")
    list_filter = ("product",)
    search_fields = ["product", "color_name"]
    raw_id_fields = ("product",)

    def short_product_name(self, obj):
        return F"{obj.product.title[:15]}..."


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'is_enable', 'created_time']
    list_editable = ['is_enable']
    date_hierarchy = "created_time"
    search_fields = ['product', 'user', 'text']
    list_filter = ['is_enable', 'product', 'parent', 'user']
    raw_id_fields = ['product', 'user', 'parent']
