from django import forms
import datetime

DURATION_CHOICES = (
    ('EOY', 'Until Year End'),
    ('M', '1 Month Only'),
)
class AddMonthlyBudget(forms.Form):
    budget = forms.CharField(widget=forms.TextInput(attrs={'size': '15'}))
    amount = forms.DecimalField(max_digits=65, decimal_places=2, widget=forms.TextInput(attrs={'size': '6'}))
    starting_month = forms.DateField(widget=forms.TextInput(attrs={'class': 'ink-datepicker', 'size': '10', 'data-start-week-day': "0"}))
    duration = forms.ChoiceField(widget=forms.RadioSelect, choices=DURATION_CHOICES)

class FilterForm(forms.Form):
    month = forms.DateField(widget=forms.TextInput(attrs={'class': 'ink-datepicker', 'data-start-week-day': "0"}))