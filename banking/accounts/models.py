from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=65, decimal_places=2)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug