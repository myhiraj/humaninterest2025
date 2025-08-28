from django.urls import path
from . import views
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('/')
app_name = 'hsa'

urlpatterns = [
    # Landing page
    path('', views.index, name='index'),
    
    # Main dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # User registration
    path('signup/', views.signup, name='signup'),
    
    # Core HSA features
    path('deposit/', views.deposit_funds, name='deposit_funds'),
    path('issue-card/', views.issue_card, name='issue_card'),
    path('transaction/', views.process_transaction, name='process_transaction'),
    path('history/', views.transaction_history, name='transaction_history'),
    path('logout/', logout_view, name='logout'),
]
