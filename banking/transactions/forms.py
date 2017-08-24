from django import forms
import datetime

from .models import Category
from budget.models import Budget, MonthlyBudget

DIRECTION_CHOICES=(
    ("O", "Out"),
    ("I", "In"),
)

class AddTransactionForm(forms.Form):
    date = forms.DateField( widget=forms.TextInput(attrs={'class': 'ink-datepicker', 'size': '10', 'data-start-week-day': "0"}))
    budget = forms.CharField()
    beneficiary = forms.CharField()
    category = forms.CharField()
    amount = forms.DecimalField(max_digits=65, decimal_places=2, localize=True, widget=forms.TextInput(attrs={'size': '6'}))
    direction = forms.ChoiceField(widget=forms.RadioSelect, choices=DIRECTION_CHOICES, initial="O")

    def __init__(self, *args, **kwargs): #Need to overide the init so that the modelchoice queryset will update each time the form loads
        super(AddTransactionForm, self).__init__(*args, **kwargs)
        self.fields['budget'] = forms.ModelChoiceField(queryset=Budget.objects.all(), required=False)
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)


class FilterForm(forms.Form):
    thirty_days_ago = datetime.datetime.today() + datetime.timedelta(-30)
    thirty_days_ago = thirty_days_ago.strftime('%Y-%m-%d')
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'ink-datepicker', 'data-start-date': thirty_days_ago, 'data-start-week-day': "0"}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'ink-datepicker', 'data-start-week-day': "0"}))