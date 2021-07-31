from django.db import models
from auth.models import User

class Category(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE) 
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name

class Expense(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.TextField()
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date = models.DateField()


