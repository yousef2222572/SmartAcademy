from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User





class TransactionStatus(models.IntegerChoices):
    Pending = 0, _('Pending')
    Delivery = 1, _('delivery')
    Completed = 2, _('Completed')
    
    
    

class PaymentMethod(models.IntegerChoices):
    Stripe = 1, _('Stripe')
    Paypal = 2, _('Paypal')
    Cash = 3, _('Cash')
    

class Transaction(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    amount = models.FloatField()
    items = models.JSONField(default=dict)
    customer = models.JSONField(default=dict)
    status=models.IntegerField(
        default=TransactionStatus.Pending,
        choices=TransactionStatus.choices
    )
    payment_method=models.IntegerField(
        choices=PaymentMethod.choices
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def customer_name(self):
        return self.customer['first_name'] + ' ' + self.customer['last_name']

    @property
    def customer_email(self):
        return self.customer['email']
    
    @property
    def customer_phone_number(self):
        return self.customer['phone_number']
    
    
class Order(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.id,)