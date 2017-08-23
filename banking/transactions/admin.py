from django.contrib import admin
from .models import Transaction, Category

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('slug', 'date', 'account', 'amount')


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category)