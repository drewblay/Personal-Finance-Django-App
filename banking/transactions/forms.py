from django import forms
import datetime

from .models import Category
from budget.models import Budget, MonthlyBudget

DIRECTION_CHOICES=(
    ("O", "Out"),
    ("I", "In"),
)
from django import forms

class EmptyChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), empty_label=None, required=True, widget=None, label=None,
                 initial=None, help_text=None, *args, **kwargs):

        # prepend an empty label if it exists (and field is not required!)
        if not required and empty_label is not None:
            choices = tuple([(u'', empty_label)] + list(choices))

        super(EmptyChoiceField, self).__init__(choices=choices, required=required, widget=widget, label=label, initial=initial, help_text=help_text, *args, **kwargs)


class AddTransactionForm(forms.Form):
    date = forms.DateField( widget=forms.TextInput(attrs={'class': 'ink-datepicker', 'size': '10'}))
    budget = forms.CharField(required=False)
    beneficiary = forms.CharField()
    category = forms.CharField(required=False)
    amount = forms.DecimalField(max_digits=100, decimal_places=2, widget=forms.TextInput(attrs={'size': '6'}))
    direction = forms.ChoiceField(widget=forms.RadioSelect, choices=DIRECTION_CHOICES, initial="O")

    def __init__(self, *args, **kwargs):
        super(AddTransactionForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
        self.fields['budget'] = forms.ModelChoiceField(queryset=Budget.objects.all(), empty_label="", required=False)


class FilterForm(forms.Form):
    thirty_days_ago = datetime.datetime.today() + datetime.timedelta(-30)
    thirty_days_ago = thirty_days_ago.strftime('%Y-%m-%d')
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'ink-datepicker', 'data-start-date': thirty_days_ago}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'ink-datepicker'}))