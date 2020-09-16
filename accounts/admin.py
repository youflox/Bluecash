from django.contrib import admin

from .models import UserDetailsModel, AddMoneyTransactionsModel, TransferMoneyTransactionsModel
# Register your models here.

admin.site.register(UserDetailsModel)
admin.site.register(AddMoneyTransactionsModel)
admin.site.register(TransferMoneyTransactionsModel)
