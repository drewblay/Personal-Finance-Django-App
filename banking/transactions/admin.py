from django.contrib import admin
from .models import Transaction, Category, PaymentTransaction, TransferTransaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('slug', 'date', 'account', 'amount')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('slug', 'date', 'beneficiary', 'account', 'amount')

class TransferAdmin(admin.ModelAdmin):
    list_display = ('slug', 'date', 'account', 'amount', 'from_account', 'to_account')

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(PaymentTransaction, PaymentAdmin)
admin.site.register(TransferTransaction, TransferAdmin)
admin.site.register(Category)