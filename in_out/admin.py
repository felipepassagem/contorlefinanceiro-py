from django.contrib import admin
from .models import Money
# Register your models here.
class DisplayMoney(admin.ModelAdmin):
    list_display = ('id', 'valor', 'payment_type', 'add_or_remove', 'category','entry_date', 'user')
    list_display_links = ('id', 'valor')
    search_fields = ('id','payment_type','category')
    list_per_page = (10)

admin.site.register(Money, DisplayMoney)