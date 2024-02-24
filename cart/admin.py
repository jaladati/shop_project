from django.contrib import admin

from cart.models import CartItem, Cart


class CartItemInline(admin.TabularInline):
    raw_id_fields = ["product"]
    model = CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "is_paid", "payment_date")
    list_filter = ("is_paid", "user")
    search_fields = ("first_name", "last_name", "phone", "address")
    list_editable = ("is_paid",)
    raw_id_fields = ("user",)
    date_hierarchy = "payment_date"
    inlines = (
        CartItemInline,
    )
