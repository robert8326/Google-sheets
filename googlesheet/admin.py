from django.contrib import admin
from googlesheet.models import (
    Receipt
)


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('source_id', 'order_id', 'price_usd', 'price_rub', 'delivery_date')
    list_display_links = ('source_id', 'order_id', 'price_usd',)
    search_fields = ('order_id',)
    date_hierarchy = 'delivery_date'
