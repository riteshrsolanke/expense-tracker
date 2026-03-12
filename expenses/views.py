
from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Sum

# expenses/views.py
from datetime import datetime

@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    # Filter by month if requested
    month_str = request.GET.get('month')  # e.g., "2026-03"
    if month_str:
        try:
            # Convert "YYYY-MM" to month integer
            month = int(month_str.split('-')[1])
            year = int(month_str.split('-')[0])
            expenses = expenses.filter(date__year=year, date__month=month)
        except:
            pass  # ignore invalid input

    
    total = expenses.aggregate(total=Sum("amount"))["total"] or 0
    context = {'expenses': expenses, 'total': total, 'selected_month': month_str}
    return render(request, 'expenses/home.html', context)
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def delete_expense(request, id):
    expense = Expense.objects.get(id=id, user=request.user)
    expense.delete()
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # this creates the user
            login(request, user)  # automatically log in the new user
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'expenses/signup.html', {'form': form})

@login_required
def graph(request):
    import json
    from django.db.models import Sum
    from django.db.models.functions import TruncMonth

    expenses = Expense.objects.filter(user=request.user)
    data = expenses.annotate(month=TruncMonth('date'))\
                   .values('month')\
                   .annotate(total=Sum('amount'))\
                   .order_by('month')

    labels = [d['month'].strftime('%B %Y') for d in data]
    totals = [d['total'] for d in data]

    return render(request, 'expenses/graph.html', {'labels': labels, 'totals': totals})