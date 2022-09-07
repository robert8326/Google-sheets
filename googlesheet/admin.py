from django.contrib import admin
from googlesheet.models import (
    Receipt
)


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    pass
