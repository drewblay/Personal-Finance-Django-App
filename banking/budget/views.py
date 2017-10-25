from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView
from django.db.models import Sum
import datetime

from .models import Budget, MonthlyBudget
from transactions.models import Transaction
from .forms import AddMonthlyBudget, FilterForm

class MonthlyBudgetOverview(View):

    def get(self, request):
        budget_form = AddMonthlyBudget(prefix='budget_form')
        filter_form = FilterForm(prefix='filter_form')
        now = datetime.datetime.now()
        monthlybudgets = MonthlyBudget.objects.filter(month__year=now.year, month__month=now.month)
        header = now.strftime('%B') + " " + str(now.year)
        planned_total = MonthlyBudget.objects.filter(month__year=now.year, month__month=now.month).aggregate(Sum('planned'))
        actual_total = MonthlyBudget.objects.filter(month__year=now.year, month__month=now.month).aggregate(Sum('actual'))
        cash_in = Transaction.objects.filter(date__year=now.year, date__month=now.month, debit=False, transfer=False).aggregate(Sum('amount'))
        cash_out = Transaction.objects.filter(date__year=now.year, date__month=now.month, debit=True, transfer=False).aggregate(
            Sum('amount'))

        context = {'cash_out': cash_out, 'cash_in': cash_in, 'monthlybudgets': monthlybudgets,'budget_form': budget_form, 'header': header, 'filter_form': filter_form, 'planned_total': planned_total, 'actual_total': actual_total}
        return render(request, 'budget/monthlybudget.html', context)

    def post(self, request):
        budget_form = AddMonthlyBudget(prefix='budget_form')
        filter_form = FilterForm(prefix='filter_form')
        now = datetime.datetime.now()
        action = self.request.POST['action']
        monthlybudgets = MonthlyBudget.objects.filter(month__year=now.year, month__month=now.month)
        header = now.strftime('%B') + " " + str(now.year)
        planned_total = MonthlyBudget.objects.filter(month__year=now.year, month__month=now.month).aggregate(Sum('planned'))
        actual_total = MonthlyBudget.objects.filter(month__year=now.year, month__month=now.month).aggregate(
            Sum('actual'))
        cash_in = Transaction.objects.filter(date__year=now.year, date__month=now.month, debit=False, transfer=False).aggregate(
            Sum('amount'))
        cash_out = Transaction.objects.filter(date__year=now.year, date__month=now.month, debit=True, transfer=False).aggregate(
            Sum('amount'))

        if (action == 'add_budget'):
            budget_form = AddMonthlyBudget(request.POST, prefix = 'budget_form')
            if budget_form.is_valid():
                budget_data = {}
                for key, value in budget_form.cleaned_data.items():
                    budget_data[key] = value
                newbudget = Budget.objects.filter(name=budget_data['budget']).first() #Look to see if the budget already exists
                if newbudget:
                    pass #if the budget exists then do nothing
                else:
                    newbudget = Budget.objects.create(name=budget_data['budget'])
                if budget_data['duration'] == 'M':
                    newmonthlybudget = MonthlyBudget.objects.create(budget=newbudget, month=budget_data['starting_month'], planned=budget_data['amount'], actual=0.00)
                else:
                    start = budget_data['starting_month']
                    start_month = int(start.month)
                    start_year = int(start.year)
                    months = []
                    while start_month < 13:
                        months.append(start_month)
                        start_month += 1
                    print(months)
                    for month in months:
                        budget_month = str(datetime.date(start_year, month, 1))
                        newmonthlybudget = MonthlyBudget.objects.create(budget=newbudget, month=budget_month, planned=budget_data['amount'], actual=0.00)
                planned_total = MonthlyBudget.objects.filter(month__year=now.year, month__month=now.month).aggregate(
                    Sum('planned'))
        elif (action == 'date_filter'):
            filter_form = FilterForm(request.POST, prefix='filter_form')
            if filter_form.is_valid():
                month = filter_form.cleaned_data['month']
                header = month.strftime('%B') + " " + str(month.year)
                monthlybudgets = MonthlyBudget.objects.filter(month__year=month.year, month__month=month.month)
                planned_total = MonthlyBudget.objects.filter(month__year=now.year, month__month=month.month).aggregate(
                    Sum('planned'))
                actual_total = MonthlyBudget.objects.filter(month__year=now.year, month__month=month.month).aggregate(
                    Sum('actual'))
            else:
                monthlybudgets = MonthlyBudget.objects.filter(month__year=now.year, month__month=now.month)

        context = {'cash_out': cash_out, 'cash_in': cash_in, 'monthlybudgets': monthlybudgets,'budget_form': budget_form, 'header': header, 'filter_form': filter_form, 'planned_total': planned_total, 'actual_total': actual_total}
        return render(request, 'budget/monthlybudget.html', context)