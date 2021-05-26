from django.db import models
from auth.models import User

class Expense(models.Model):

    CATEGORIES = [
        ("CATEGORY_1", "Category #1"),
        ("CATEGORY_2", "Category #2"),
        ("CATEGORY_3", "Category #3"),
        ("CATEGORY_4", "Category #4"),
    ]

    category = models.CharField(max_length=127, choices=CATEGORIES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
