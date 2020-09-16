from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator


class UserDetailsModel(models.Model):
    phone = models.BigIntegerField(null=False, unique=True, validators=[MinValueValidator(1000000000),MaxValueValidator(9999999999)])
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.OneToOneField(get_user_model(),primary_key='email' , on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class AddMoneyTransactionsModel(models.Model):
    credited = models.DecimalField(max_digits=10, decimal_places=2,null=False,blank=False)
    time = models.DateTimeField(auto_now_add=True, editable=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.user)


class TransferMoneyTransactionsModel(models.Model):
    to = models.CharField(null=False, blank=False,max_length=10)
    debited = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True, editable=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.user)
