# hsa/admin.py
from django.contrib import admin
from .models import HSAAccount, HSACard, Transaction, MedicalExpenseCategory

@admin.register(MedicalExpenseCategory)
class MedicalExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_qualified', 'description']
    list_filter = ['is_qualified']
    search_fields = ['name', 'description']

@admin.register(HSAAccount)
class HSAAccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'user', 'balance', 'created_at']
    list_filter = ['created_at']
    search_fields = ['account_number', 'user__username', 'user__email']
    readonly_fields = ['account_number', 'created_at']

@admin.register(HSACard)
class HSACardAdmin(admin.ModelAdmin):
    list_display = ['masked_card_number', 'account', 'status', 'expiry_date', 'issued_at']
    list_filter = ['status', 'issued_at']
    search_fields = ['card_number', 'account__account_number', 'account__user__username']
    readonly_fields = ['card_number', 'cvv', 'expiry_date', 'issued_at']
    
    def masked_card_number(self, obj):
        return obj.masked_card_number()
    masked_card_number.short_description = 'Card Number'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'transaction_type', 'amount', 'merchant', 'status', 'transaction_date']
    list_filter = ['transaction_type', 'status', 'expense_category', 'transaction_date']
    search_fields = ['merchant', 'account__account_number', 'account__user__username']
    readonly_fields = ['transaction_date']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('account', 'card', 'expense_category')
    