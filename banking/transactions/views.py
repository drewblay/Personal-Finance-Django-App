from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView, FormView
from django.db.models import Sum
import datetime

from .models import Transaction
from accounts.models import Account
from .forms import AddTransactionForm, FilterForm
from budget.models import MonthlyBudget


class AccountTransactions(View): #View transactions from a single account

    def get_context_data(self, *args, **kwargs):
        transaction_form = AddTransactionForm(prefix='transaction_form')
        filter_form = FilterForm(prefix='filter_form')
        accountobj = Account.objects.get(slug=kwargs['account'])
        today = datetime.datetime.today().strftime('%Y-%m-%d')

        thirty_days_ago = datetime.datetime.today() + datetime.timedelta(-30)
        thirty_days_ago = thirty_days_ago.strftime('%Y-%m-%d')

        start_date = kwargs['start_date']
        end_date = kwargs['end_date']

        if start_date == 0 and end_date == 0:
            transactions = Transaction.objects.filter(account=accountobj, date__range=[thirty_days_ago, today]).order_by('date', 'id')
            total_transactions = Transaction.objects.filter(account=accountobj, date__gte=thirty_days_ago).order_by('date', 'id').reverse()
        else:
            transactions = Transaction.objects.filter(account=accountobj, date__range=[start_date, end_date]).order_by('date', 'id')
            total_transactions = Transaction.objects.filter(account=accountobj, date__gte=start_date).order_by('date', 'id').reverse()

        balances = {}
        balance = accountobj.balance

        for item in total_transactions:
            balances[item.id] = balance
            if item.debit == True:
                balance = item.amount + balance
            elif item.debit == False:
                balance = balance - item .amount

        context = {'transactions': transactions, 'account': accountobj, 'transaction_form': transaction_form, 'filter_form': filter_form, 'balances': balances}
        return context


    def get(self, request, account):
        start_date = 0
        end_date = 0

        return render(request, 'transactions/overview.html', self.get_context_data(request, account=account, start_date=start_date, end_date=end_date))


    def post(self, request, account):
        action = self.request.POST['action']
        accountobj = Account.objects.get(slug = account)
        start_date =0
        end_date = 0

        if (action == 'add_transaction'):
            transaction_form = AddTransactionForm(request.POST, prefix='transaction_form')
            if transaction_form.is_valid():
                transaction_data = {'account': accountobj}
                for key, value in transaction_form.cleaned_data.items():
                    ###Handle special fields###
                    if key == "budget":# If the transaction is applied towards a budget:
                        #The transaction will hit the monthly budget for the month the transaction is posted in
                        #If you are paying something for next months budget (i.e. paying the mortgage due the 1st)
                        #then you need to post-date the transaction to the next month
                        if value != None: #If the budget value is not NONE
                            date = transaction_form.cleaned_data['date']
                            year = date.year
                            month = date.month
                            #Get the budget for the month and year of the transaction
                            budget = MonthlyBudget.objects.filter(budget__slug=value, month__year=year, month__month=month).first()
                            if budget:
                                transaction_data[key] = budget #pass the instance of the monthly budget
                                #Apply the transaction to the monthly budget
                                new_budget_actual = budget.actual + transaction_form.cleaned_data['amount']
                                budget.actual = new_budget_actual
                                budget.save()
                            else: #Otherwise show an error notifying the user that no instance of the budget for the given month and year
                                month = date.strftime('%B')
                                error = "Error: There is no {} budget for {}. {}. Please add the budget then resubmit the transaction.".format(value, month, year) #if there is no matching budget set the value to Error
                                context = {'transaction_form': transaction_form, 'error': error, 'account': accountobj, 'filter_form': filter_form}
                                return render(request, 'transactions\overview.html', context)
                    elif key == "direction": #Convert the direction to either True or False for the debit field
                        if value == "O": #If money is going OUT it is a debit
                            transaction_data["debit"] = True
                        else: #If money is coming in it is not a debit
                            transaction_data["debit"] = False
                    ###If there is nothing special with the field just add the key and value to the dictionary###
                    else:
                        transaction_data[key] = value
                if transaction_form.cleaned_data['direction'] == 'O': #Check the direction of money flow and update the balance of the account
                    new_balance = accountobj.balance - transaction_data['amount'] #Money is going out
                else:
                    new_balance = accountobj.balance + transaction_data['amount'] #Money coming in
                transaction_data['balance'] = new_balance
                Transaction.objects.create(**transaction_data)  # Create the transaction from the dictionary
                accountobj.balance = new_balance
                accountobj.save()
            else:
                error = "There was an error with the form"
                context = {'transaction_form': transaction_form, 'error': error, 'account': accountobj,
                           'filter_form': filter_form}
                return render(request, 'transactions\overview.html', context)

        elif (action == 'date_filter'):
            filter_form = FilterForm(request.POST, prefix='filter_form')
            if filter_form.is_valid():
                start_date = filter_form.cleaned_data['start_date']
                end_date = filter_form.cleaned_data['end_date']
                transactions = Transaction.objects.filter(account = accountobj, date__range=[start_date, end_date]).order_by('date')
        else:
            transactions = Transaction.objects.filter(account = accountobj, date__range=[thirty_days_ago, today]).order_by('date')

        return render(request, 'transactions/overview.html',  self.get_context_data(request, account=account, start_date=start_date, end_date=end_date))