from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView, FormView
import datetime

from .models import Transaction, PaymentTransaction
from accounts.models import Account
from .forms import AddTransactionForm, FilterForm
from budget.models import MonthlyBudget

class AllTransactions(View): #This is a view of transactions from ALL accounts

    def get(self, request):
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        thirty_days_ago = datetime.datetime.today() + datetime.timedelta(-30)
        thirty_days_ago = thirty_days_ago.strftime('%Y-%m-%d')
        transactions = Transaction.objects.filter(date__range=[thirty_days_ago, today])

        context = {'transactions': transactions}
        return render(request, 'transactions/overview.html', context)


class AccountTransactions(View): #View transactions from a single account

    def get(self, request, account):
        transaction_form = AddTransactionForm(prefix='transaction_form')
        filter_form = FilterForm(prefix='filter_form')
        accountobj = Account.objects.get(slug = account)
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        thirty_days_ago = datetime.datetime.today() + datetime.timedelta(-30)
        thirty_days_ago = thirty_days_ago.strftime('%Y-%m-%d')
        transactions = Transaction.objects.filter(account = accountobj, date__range=[thirty_days_ago, today])

        context = {'transactions': transactions, 'account': accountobj, 'transaction_form': transaction_form, 'filter_form': filter_form}
        return render(request, 'transactions/overview.html', context)

    def post(self, request, account):

        transaction_form = AddTransactionForm(prefix='transaction_form')
        filter_form = FilterForm(prefix='filter_form')
        action = self.request.POST['action']
        accountobj = Account.objects.get(slug = account)
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        thirty_days_ago = datetime.datetime.today() + datetime.timedelta(-30)
        thirty_days_ago = thirty_days_ago.strftime('%Y-%m-%d')
        transactions = Transaction.objects.filter(account = accountobj, date__range=[thirty_days_ago, today])

        if (action == 'add_transaction'):
            transaction_form = AddTransactionForm(request.POST, prefix='transaction_form')
            if transaction_form.is_valid():
                transaction_data = {'account': accountobj}
                for key, value in transaction_form.cleaned_data.items():
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
                                budget.actual = transaction_form.cleaned_data['amount']
                                budget.save()
                            else: #Show an error notifying the user that no instance of the budget exists for that month and year
                                month = date.strftime('%B')
                                error = "Error: There is no {} budget for {}. {}. Please add the budget then resubmit the transaction.".format(value, month, year) #if there is no matching budget set the value to Error
                                context = {'transaction_form': transaction_form, 'error': error, 'account': accountobj, 'filter_form': filter_form}
                                return render(request, 'transactions\overview.html', context)
                    elif key == "direction": #We don't want the direction in transaction data dictionary as this is not a field
                        pass
                    else:
                        transaction_data[key] = value
                PaymentTransaction.objects.create(**transaction_data) #Create the transaction for the dictionary

                if transaction_form.cleaned_data['direction'] == 'O': #Check the direction of money flow and update the balance of the account
                    new_balance = accountobj.balance - transaction_data['amount'] #Money is going out
                else:
                    new_balance = accountobj.balance + transaction_data['amount'] #Money coming in
                accountobj.balance = new_balance
                accountobj.save()

        elif (action == 'date_filter'):
            filter_form = FilterForm(request.POST, prefix='filter_form')
            if filter_form.is_valid():
                start_date = filter_form.cleaned_data['start_date']
                end_date = filter_form.cleaned_data['end_date']
                transactions = Transaction.objects.filter(account = accountobj, date__range=[start_date, end_date])
        else:
            transactions = Transaction.objects.filter(account = accountobj, date__range=[thirty_days_ago, today])

        context = {'transaction_form': transaction_form, 'transactions': transactions, 'account': accountobj, 'filter_form': filter_form}
        return render(request, 'transactions/overview.html', context)