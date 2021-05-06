from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.conf import settings

class Money(models.Model):
    CATEGORY_LIST = (
        ('Outro', 'Outro'),
        ('Trabalho', 'Trabalho'),
        ('Lazer', 'Lazer'),
        ('Aluguel', 'Aluguel'),
        ('Gastos Pessoais', 'Gastos Pessoais'),
        ('Investimentos', 'Investimentos')
    )
    PAYMENT_TYPE = (
        ('Dinheiro','Dinheiro'),
        ('Cartão','Cartão'),
        ('Cheque','Cheque'),
        ('Outro','Outro'),
    )
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    valor = models.DecimalField(decimal_places=2, max_digits=8, blank=False)
    entry_date = models.DateField(default=1, blank=True)
    add_or_remove = models.BooleanField(default=True)
    category = models.CharField(max_length=50, choices=CATEGORY_LIST, blank=False)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE)
    obs = models.TextField(max_length=80, blank=True)