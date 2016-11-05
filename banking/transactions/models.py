from django.db import models
from django.utils.text import slugify
from polymorphic.models import PolymorphicModel

from accounts.models import Account
from budget.models import MonthlyBudget



class Transaction(PolymorphicModel):
    date = models.DateField()
    account = models.ForeignKey(Account)
    budget = models.ForeignKey(MonthlyBudget, blank=True, null=True)
    category = models.ForeignKey('Category')
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        forslug = "{0.date}-{0.account}-{0.amount}".format(self)
        self.slug = slugify(forslug)
        super(Transaction, self).save()

class PaymentTransaction(Transaction):
    beneficiary = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        forslug = "{0.date}-{0.account}-{0.beneficiary}-{0.amount}".format(self)
        self.slug = slugify(forslug)
        super(PaymentTransaction, self).save()

class TransferTransaction(Transaction):
    from_account = models.ForeignKey(Account, related_name='from_account')
    to_account = models.ForeignKey(Account, related_name='to_account')

    def save(self, *args, **kwargs):
        forslug = "{0.date}-{0.account}-Transfer-{0.amount}".format(self)
        self.slug = slugify(forslug)
        super(TransferTransaction, self).save()

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save()

    def __str__(self):
        return self.slug