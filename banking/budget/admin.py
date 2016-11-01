from django.contrib import admin
from .models import Budget, MonthlyBudget, SavingsGoal

admin.site.register(Budget)
admin.site.register(MonthlyBudget)
admin.site.register(SavingsGoal)