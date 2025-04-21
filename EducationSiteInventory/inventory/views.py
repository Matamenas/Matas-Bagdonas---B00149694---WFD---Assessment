from django.shortcuts import render, redirect
from .models import Item, ItemRequest
from .forms import ItemRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('teacher_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
@login_required
def teacher_dashboard(request):
    return render(request, 'inventory/teacher_dashboard.html')

@login_required
def request_item(request):
    if request.method == 'POST':
        form = ItemRequestForm(request.POST)
        if form.is_valid():
            item_request = form.save(commit=False)
            item_request.teacher = request.user
            item_request.save()
            return redirect('my_requests')
    else:
        form = ItemRequestForm()
    return render(request, 'inventory/request_item.html', {'form': form})

@login_required
def my_requests(request):
    requests = ItemRequest.objects.filter(teacher=request.user)
    return render(request, 'inventory/my_requests.html', {'requests': requests})

