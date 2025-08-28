from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import random
import string
from datetime import date, timedelta

# Create your models here.

# hsa/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import random
import string
from datetime import date, timedelta

class MedicalExpenseCategory(models.Model):
    """IRS-qualified medical expense categories for transaction validation"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_qualified = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Medical Expense Categories"
    
    def __str__(self):
        return self.name

class HSAAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)
    
    def generate_account_number(self):
        return 'HSA' + ''.join(random.choices(string.digits, k=10))
    
    def __str__(self):
        return f"HSA Account {self.account_number} - {self.user.username}"

class HSACard(models.Model):
    CARD_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('blocked', 'Blocked'),
        ('expired', 'Expired'),
    ]
    
    account = models.ForeignKey(HSAAccount, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=16, unique=True)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=3)
    status = models.CharField(max_length=20, choices=CARD_STATUS_CHOICES, default='pending')
    issued_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.card_number:
            self.card_number = self.generate_card_number()
        if not self.cvv:
            self.cvv = self.generate_cvv()
        if not self.expiry_date:
            self.expiry_date = date.today() + timedelta(days=365*3)  # 3 years from now
        super().save(*args, **kwargs)
    
    def generate_card_number(self):
        # Generate a fake 16-digit card number starting with 4 (Visa-like)
        return '4' + ''.join(random.choices(string.digits, k=15))
    
    def generate_cvv(self):
        return ''.join(random.choices(string.digits, k=3))
    
    def masked_card_number(self):
        return f"****-****-****-{self.card_number[-4:]}"
    
    def __str__(self):
        return f"Card {self.masked_card_number()} - {self.account.user.username}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('purchase', 'Purchase'),
        ('deposit', 'Deposit'),
        ('refund', 'Refund'),
    ]
    
    TRANSACTION_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('refunded', 'Refunded'),
    ]
    
    account = models.ForeignKey(HSAAccount, on_delete=models.CASCADE, related_name='transactions')
    card = models.ForeignKey(HSACard, on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    merchant = models.CharField(max_length=255, blank=True)
    expense_category = models.ForeignKey(MedicalExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='pending')
    decline_reason = models.CharField(max_length=255, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-transaction_date']
    
    def __str__(self):
        return f"{self.transaction_type.title()} - ${self.amount} - {self.merchant or 'N/A'}"


