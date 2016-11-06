from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView
from django.db.models import Sum
import datetime

from .models import Account
from .forms import TransferForm
from transactions.models import Transaction, Category

class AccountsOverview(View):

    def get(self, request):
        transfer_form = TransferForm(prefix='transfer_form')
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

        context = {'accounts': accounts, 'chart_data': chart_data, 'transfer_form': transfer_form}
        return render(request, 'accounts/overview.html', context)

    def post(self, request):
        accounts = Account.objects.all()
        categorys = Category.objects.all()
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        thirty_days_ago = datetime.datetime.today() + datetime.timedelta(-30)
        thirty_days_ago = thirty_days_ago.strftime('%Y-%m-%d')

        chart_data = {}
        for category in categorys:
            if Transaction.objects.filter(category=category.id,
                                          date__range=[thirty_days_ago, today]).count() and category.name != 'income':
                amount = Transaction.objects.filter(category=category.id).aggregate(Sum('amount'))
                chart_data[category.name] = amount['amount__sum']
            elif category.name == 'income':
                pass
            else:
                chart_data[category.name] = 0
        transfer_form = TransferForm(request.POST, prefix='transfer_form')
        if transfer_form.is_valid():
            transfer_data = {}
            for key, value in transfer_form.cleaned_data.items():
                transfer_data[key] = value
            from_acct_new_bal = transfer_data['from_acct'].balance - transfer_data['amount']
            transfer_data['from_acct'].balance = from_acct_new_bal
            transfer_data['from_acct'].save()
            to_acct_new_bal = transfer_data['to_acct'].balance + transfer_data['amount']
            transfer_data['to_acct'].balance = to_acct_new_bal
            transfer_data['to_acct'].save()
        else:
            print("the form is not valid you dumb shit")

        context = {'accounts': accounts, 'chart_data': chart_data, 'transfer_form': transfer_form}
        return render(request, 'accounts/overview.html', context)
