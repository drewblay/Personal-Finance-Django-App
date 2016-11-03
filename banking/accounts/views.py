from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView
from django.db.models import Sum
import datetime

from .models import Account
from transactions.models import Transaction, Category

class AccountsOverview(View):

    def get(self, request):
        accounts = Account.objects.all()
        categorys = Category.objects.all()
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        thirty_days_ago = datetime.datetime.today() + datetime.timedelta(-30)
        thirty_days_ago = thirty_days_ago.strftime('%Y-%m-%d')

        chart_data = {}
        for category in categorys:
            if Transaction.objects.filter(category=category.id, date__range=[thirty_days_ago, today]).count() and category.name != 'income':
                amount = Transaction.objects.filter(category=category.id).aggregate(Sum('amount'))
                chart_data[category.name] = amount['amount__sum']
            elif category.name == 'income':
                pass
            else:
                chart_data[category.name] = 0

        context = {'accounts': accounts, 'chart_data': chart_data}
        return render(request, 'accounts/overview.html', context)