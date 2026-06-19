from django.contrib import admin
from .models import AcceptedProduct

@admin.register(AcceptedProduct)
class AcceptedProductAdmin(admin.ModelAdmin):

    list_display = (
        'product_name',
        'retailer',
        'wholesaler',
        'accepted_at'
    )

    search_fields = (
        'product_name',
        'retailer__username',
        'wholesaler__username'
    )