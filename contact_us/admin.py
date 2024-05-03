from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["subject", "name", "phone", "read_by_admin"]
    list_editable = ["read_by_admin"]
    list_filter = ["subject", "read_by_admin"]
    search_fields = ["message", "name", "phone", "email"]
