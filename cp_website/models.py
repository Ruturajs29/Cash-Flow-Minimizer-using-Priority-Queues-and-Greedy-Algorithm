# models.py
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    debtor = models.ForeignKey(Person, related_name='debts', on_delete=models.CASCADE)
    creditor = models.ForeignKey(Person, related_name='credits', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.debtor.name} owes {self.creditor.name} Rs {self.amount}"