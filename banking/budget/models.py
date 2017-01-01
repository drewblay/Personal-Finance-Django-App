from django.db import models
from django.utils.text import slugify

class Budget(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Budget, self).save()

class MonthlyBudget(models.Model):
    budget = models.ForeignKey('Budget')
    month = models.DateField()
    planned = models.DecimalField(max_digits=65, decimal_places=2)
    actual = models.DecimalField(max_digits=65, decimal_places=2, blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        forslug = "{0.budget}-{0.month}".format(self)
        self.slug = slugify(forslug)
        super(MonthlyBudget, self).save()

#TO DO Add savings goals