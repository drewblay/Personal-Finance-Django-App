from django import forms
from django.forms import ModelChoiceField

from .models import Account


class TransferChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class TransferForm(forms.Form):
    date = forms.DateField( widget=forms.TextInput(attrs={'class': 'ink-datepicker', 'size': '10'}))
    from_acct = TransferChoiceField(queryset=Account.objects.all())
    to_acct = TransferChoiceField(queryset=Account.objects.all())
    amount = forms.DecimalField(max_digits=65, decimal_places=2, widget=forms.TextInput(attrs={'size': '6'}))