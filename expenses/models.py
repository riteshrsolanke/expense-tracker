
from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    reason = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.reason}"