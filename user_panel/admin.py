from django.contrib import admin

from .models import UserProductList


@admin.register(UserProductList)
class UserProductListAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']
    list_editable = ['user']
    search_fields = ['title', 'description']
    list_filter = ['user', 'products']
    raw_id_fields = ['user', 'products']
