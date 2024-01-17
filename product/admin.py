from django.contrib import admin
from .models import *
from django_jalali import admin as jadmin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['title', 'is_enable']
    readonly_fields = ['slug']
    list_editable = ['is_enable']
    list_filter = ['is_enable', 'parent']
    search_fields = ['title']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['short_title', 'price', 'off', 'size', 'stock_count']
    readonly_fields = ['created_time', 'updated_time', 'stock_count']
    list_editable = ['price', 'off', 'size']
    date_hierarchy = "created_time"
    search_fields = ['title', 'short_description', 'description']
    list_filter = ['category']
    raw_id_fields = ['category']

    def short_title(self, obj):
        return F"{obj.title[:15]}..."



@admin.register(ProductColorVariant)
class ProductColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'stock_count']
    list_editable = ['stock_count']
    search_fields = ['color_name', 'color_hex_code']