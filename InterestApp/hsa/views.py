from django.shortcuts import render

# hsa/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from decimal import Decimal
import json

from .models import HSAAccount, HSACard, Transaction, MedicalExpenseCategory

def index(request):
    """Landing page for HSA application"""
    if request.user.is_authenticated:
        # If user is logged in, show their basic info
        try:
            hsa_account = request.user.hsaaccount
        except HSAAccount.DoesNotExist:
            hsa_account = None
        
        context = {
            'hsa_account': hsa_account,
        }
    else:
        context = {}
    
    return render(request, 'hsa/index.html', context)

def signup(request):
    """User registration and HSA account creation"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically create HSA account for new user
            hsa_account = HSAAccount.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Account created successfully! Your HSA account number is {hsa_account.account_number}')
            return redirect('hsa:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard(request):
    """Main HSA dashboard"""
    try:
        hsa_account = request.user.hsaaccount
    except HSAAccount.DoesNotExist:
        # Create HSA account if it doesn't exist
        hsa_account = HSAAccount.objects.create(user=request.user)
        messages.info(request, f'HSA account created! Account number: {hsa_account.account_number}')
    
    recent_transactions = hsa_account.transactions.all()[:5]
    active_cards = hsa_account.cards.filter(status='active')
    
    context = {
        'hsa_account': hsa_account,
        'recent_transactions': recent_transactions,
        'active_cards': active_cards,
    }
    return render(request, 'hsa/dashboard.html', context)

@login_required
def deposit_funds(request):
    """Deposit funds into HSA account"""
    hsa_account = get_object_or_404(HSAAccount, user=request.user)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = Decimal(amount)
            if amount <= 0:
                messages.error(request, 'Amount must be greater than zero.')
            else:
                # Create deposit transaction
                Transaction.objects.create(
                    account=hsa_account,
                    transaction_type='deposit',
                    amount=amount,
                    description='Account funding',
                    status='approved'
                )
                # Update account balance
                hsa_account.balance += amount
                hsa_account.save()
                messages.success(request, f'Successfully deposited ${amount} into your HSA account.')
                return redirect('hsa:dashboard')
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid amount.')
    
    active_cards = hsa_account.cards.filter(status='active')
    
    return render(request, 'hsa/deposit_funds.html', {
        'hsa_account': hsa_account,
        'active_cards': active_cards
        })

@login_required
def issue_card(request):
    """Issue a new HSA debit card"""
    hsa_account = get_object_or_404(HSAAccount, user=request.user)
    
    if request.method == 'POST':
        # Check if user already has an active card
        existing_card = hsa_account.cards.filter(status__in=['active', 'pending']).first()
        if existing_card:
            messages.warning(request, 'You already have an active or pending card.')
        else:
            # Issue new card
            new_card = HSACard.objects.create(
                account=hsa_account,
                status='active'  # For demo purposes, make it active immediately
            )
            messages.success(request, f'New HSA card issued successfully! Card ending in {new_card.card_number[-4:]}')
        return redirect('hsa:dashboard')
    
    existing_cards = hsa_account.cards.all()
    return render(request, 'hsa/issue_card.html', {
        'hsa_account': hsa_account,
        'existing_cards': existing_cards
    })

@login_required
def process_transaction(request):
    """Simulate a purchase transaction"""
    hsa_account = get_object_or_404(HSAAccount, user=request.user)
    active_card = hsa_account.cards.filter(status='active').first()
    
    if not active_card:
        messages.error(request, 'No active card found. Please request a card first.')
        return redirect('hsa:issue_card')
    
    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        merchant = request.POST.get('merchant', '').strip()
        category_id = request.POST.get('expense_category', '').strip()
        
        # Debug print - remove after fixing
        print(f"Raw amount from form: '{amount_str}' (type: {type(amount_str)})")
        
        # Clean the amount string
        if amount_str:
            amount_str = str(amount_str).strip()
        
        # Validate inputs
        if not amount_str or amount_str == '':
            messages.error(request, 'Please enter an amount.')
            return render(request, 'hsa/process_transaction.html', {
                'hsa_account': hsa_account,
                'active_card': active_card,
                'expense_categories': MedicalExpenseCategory.objects.all()
            })
        
        if not merchant:
            messages.error(request, 'Please enter a merchant name.')
            return render(request, 'hsa/process_transaction.html', {
                'hsa_account': hsa_account,
                'active_card': active_card,
                'expense_categories': MedicalExpenseCategory.objects.all()
            })
        
        if not category_id:
            messages.error(request, 'Please select an expense category.')
            return render(request, 'hsa/process_transaction.html', {
                'hsa_account': hsa_account,
                'active_card': active_card,
                'expense_categories': MedicalExpenseCategory.objects.all()
            })
        
        try:
            # Try multiple ways to convert to Decimal
            amount = Decimal(amount_str)
            print(f"Converted amount: {amount}")
            
            if amount <= Decimal('0'):
                messages.error(request, 'Amount must be greater than zero.')
                return render(request, 'hsa/process_transaction.html', {
                    'hsa_account': hsa_account,
                    'active_card': active_card,
                    'expense_categories': MedicalExpenseCategory.objects.all()
                })
            
            # Rest of your existing logic...
            # Get expense category
            try:
                expense_category = MedicalExpenseCategory.objects.get(id=category_id)
            except MedicalExpenseCategory.DoesNotExist:
                messages.error(request, 'Invalid expense category selected.')
                return render(request, 'hsa/process_transaction.html', {
                    'hsa_account': hsa_account,
                    'active_card': active_card,
                    'expense_categories': MedicalExpenseCategory.objects.all()
                })
            
            # Validate transaction
            if hsa_account.balance < amount:
                transaction = Transaction.objects.create(
                    account=hsa_account,
                    card=active_card,
                    transaction_type='purchase',
                    amount=amount,
                    merchant=merchant,
                    expense_category=expense_category,
                    status='declined',
                    decline_reason='Insufficient funds'
                )
                messages.error(request, 'Transaction declined: Insufficient funds.')
            elif not expense_category.is_qualified:
                transaction = Transaction.objects.create(
                    account=hsa_account,
                    card=active_card,
                    transaction_type='purchase',
                    amount=amount,
                    merchant=merchant,
                    expense_category=expense_category,
                    status='declined',
                    decline_reason='Not an IRS-qualified medical expense'
                )
                messages.error(request, 'Transaction declined: Not an IRS-qualified medical expense.')
            else:
                transaction = Transaction.objects.create(
                    account=hsa_account,
                    card=active_card,
                    transaction_type='purchase',
                    amount=amount,
                    merchant=merchant,
                    expense_category=expense_category,
                    status='approved'
                )
                hsa_account.balance -= amount
                hsa_account.save()
                messages.success(request, f'Transaction approved! ${amount} charged to {merchant}.')
            
            return redirect('hsa:dashboard')
            
        except (ValueError, TypeError, Exception) as e:
            print(f"Error converting amount: {e}")
            messages.error(request, f'Please enter a valid amount. Error: {str(e)}')
            return render(request, 'hsa/process_transaction.html', {
                'hsa_account': hsa_account,
                'active_card': active_card,
                'expense_categories': MedicalExpenseCategory.objects.all()
            })
    
    expense_categories = MedicalExpenseCategory.objects.all()
    return render(request, 'hsa/process_transaction.html', {
        'hsa_account': hsa_account,
        'active_card': active_card,
        'expense_categories': expense_categories
    })

@login_required
def transaction_history(request):
    """View transaction history"""
    hsa_account = get_object_or_404(HSAAccount, user=request.user)
    transactions = hsa_account.transactions.all()
    
    return render(request, 'hsa/transaction_history.html', {
        'hsa_account': hsa_account,
        'transactions': transactions
    })
