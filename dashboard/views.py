from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from core.models import TimeEntry
from .forms import TimeEntryEditForm, TimeEntryCreateForm

# Create your views here.

def home(request):
    """Strona główna przekierowuje na login."""
    return redirect('login')

@login_required
def dashboard(request):
    """Panel główny dla zalogowanych użytkowników."""
    user_role = request.user.profile.panel_role
    current_entry = TimeEntry.objects.filter(
        employee=request.user.profile,
        end_time__isnull=True
    ).first()
    
    if user_role == 'Admin':
        # Dla administratora pokazujemy wszystkie wpisy
        recent_entries = TimeEntry.objects.all().order_by('-start_time')[:10]
    elif user_role == 'Manager':
        # Dla managera pokazujemy wpisy jego podwładnych
        subordinates = request.user.profile.subordinates.all()
        recent_entries = TimeEntry.objects.filter(
            employee__in=subordinates
        ).order_by('-start_time')[:10]
    else:
        # Dla zwykłego pracownika pokazujemy tylko jego wpisy
        recent_entries = TimeEntry.objects.filter(
            employee=request.user.profile
        ).order_by('-start_time')[:5]
    
    context = {
        'current_entry': current_entry,
        'recent_entries': recent_entries,
        'user_role': user_role,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def time_entries(request):
    """Lista wszystkich wpisów czasu pracy."""
    entries = TimeEntry.objects.filter(
        employee=request.user.profile
    ).order_by('-start_time')
    
    context = {
        'entries': entries,
    }
    return render(request, 'dashboard/time_entries.html', context)

@login_required
def start_shift(request):
    """Rozpoczęcie służby."""
    if request.method == 'POST':
        # Sprawdź czy nie ma już aktywnej służby
        active_entry = TimeEntry.objects.filter(
            employee=request.user.profile,
            end_time__isnull=True
        ).first()
        
        if active_entry:
            messages.error(request, 'Masz już aktywną służbę!')
            return redirect('dashboard')
        
        # Utwórz nowy wpis
        TimeEntry.objects.create(
            employee=request.user.profile,
            start_time=timezone.now(),
        )
        messages.success(request, 'Służba rozpoczęta!')
        return redirect('dashboard')
    
    return redirect('dashboard')

@login_required
def end_shift(request):
    """Zakończenie służby."""
    if request.method == 'POST':
        active_entry = TimeEntry.objects.filter(
            employee=request.user.profile,
            end_time__isnull=True
        ).first()
        
        if not active_entry:
            messages.error(request, 'Nie masz aktywnej służby!')
            return redirect('dashboard')
        
        active_entry.end_time = timezone.now()
        active_entry.save()
        messages.success(request, 'Służba zakończona!')
        
    return redirect('dashboard')

@login_required
def delete_time_entry(request, entry_id):
    """Usuwanie wpisu czasu pracy."""
    entry = get_object_or_404(TimeEntry, id=entry_id, employee=request.user.profile)
    
    if request.method == 'POST':
        if entry.status == 'Approved':
            messages.error(request, 'Nie można usunąć zatwierdzonego wpisu!')
            return redirect('time_entries')
            
        entry.delete()
        messages.success(request, 'Wpis został usunięty.')
        return redirect('time_entries')
        
    return redirect('time_entries')

@login_required
def edit_time_entry(request, entry_id):
    """Edycja wpisu czasu pracy."""
    # Pobierz wpis
    if request.user.profile.panel_role == 'Admin':
        entry = get_object_or_404(TimeEntry, id=entry_id)
    else:
        entry = get_object_or_404(TimeEntry, id=entry_id, employee=request.user.profile)
    
    # Sprawdź czy można edytować
    if entry.status == 'Approved' and request.user.profile.panel_role != 'Admin':
        messages.error(request, 'Nie można edytować zatwierdzonego wpisu!')
        return redirect('time_entries')
    
    if request.method == 'POST':
        form = TimeEntryEditForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Wpis został zaktualizowany.')
            return redirect('time_entries')
    else:
        form = TimeEntryEditForm(instance=entry)
    
    context = {
        'form': form,
        'entry': entry,
        'is_new': False
    }
    return render(request, 'dashboard/time_entry_form.html', context)

@login_required
def admin_time_entries(request):
    """Panel administratora z wszystkimi wpisami."""
    if request.user.profile.panel_role != 'Admin':
        messages.error(request, 'Brak dostępu do panelu administratora.')
        return redirect('dashboard')
        
    entries = TimeEntry.objects.all().order_by('-start_time')
    context = {
        'entries': entries,
    }
    return render(request, 'dashboard/admin_time_entries.html', context)

@login_required
def create_time_entry(request):
    """Tworzenie nowego wpisu czasu pracy."""
    if request.method == 'POST':
        form = TimeEntryCreateForm(request.POST)
        if form.is_valid():
            time_entry = form.save(commit=False)
            time_entry.employee = request.user.profile
            time_entry.status = 'Pending'
            time_entry.save()
            messages.success(request, 'Wpis został utworzony.')
            return redirect('time_entries')
    else:
        # Domyślnie ustaw aktualną datę i godzinę
        form = TimeEntryCreateForm(initial={
            'start_time': timezone.now().strftime('%Y-%m-%dT%H:%M')
        })
    
    context = {
        'form': form,
        'is_new': True
    }
    return render(request, 'dashboard/time_entry_form.html', context)
