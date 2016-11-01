from django.contrib import admin
from .models import Transaction, Category, PaymentTransaction, TransferTransaction

admin.site.register(Transaction)
admin.site.register(PaymentTransaction)
admin.site.register(TransferTransaction)
admin.site.register(Category)

# Register your models here.
