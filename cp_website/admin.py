from django.contrib import admin
from .models import Person, Transaction

# Register Person and Transaction models
admin.site.register(Person)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('debtor', 'creditor', 'amount')
    search_fields = ('debtor__name', 'creditor__name')

admin.site.register(Transaction, TransactionAdmin)
