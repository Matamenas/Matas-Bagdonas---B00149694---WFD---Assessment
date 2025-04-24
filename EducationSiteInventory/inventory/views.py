from pyexpat.errors import messages

from .models import Item, ItemRequest
from .forms import ItemRequestForm
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm
from django.contrib import messages



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')

            # add user to corresponding group
            group = Group.objects.get(name=role)
            user.save()
            user.groups.add(group)
            login(request, user)

            return redirect('teacher_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'inventory/item_list.html', {'items': items})

@login_required
def add_item(request):

    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('item_list')
    return render(request, 'inventory/item_form.html', {'form': form})

@login_required
def edit_item(request, pk):

    item = get_object_or_404(Item, pk=pk)
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('item_list')
    return render(request, 'inventory/item_form.html', {'form': form})

@login_required
def delete_item(request, pk):

    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return redirect('item_list')

@login_required
def view_requests(request):
    requests = ItemRequest.objects.all().order_by('-created_at')
    return render(request, 'inventory/view_requests.html', {'requests': requests})

@login_required
def approve_requests(request, request_id):
    req = get_object_or_404(ItemRequest, pk=request_id)

    if req.status != 'approved':
        item = req.item

        if req.quantity_requested <= item.quantity:
            item.quantity -= req.quantity_requested
            item.save()

            req.status = 'approved'
            req.save()

            messages.success(request, f'{item.name} x{req.quantity_requested} has been approved')
        else:
            messages.error(request, f"Not enough '{item.name}' in inventory to approve request.")

    return redirect('view_requests')

@login_required
def reject_requests(request, request_id):
    req = get_object_or_404(ItemRequest, pk=request_id)
    req.status = 'rejected'
    req.save()
    return redirect('view_requests')

@login_required
def teacher_dashboard(request):
    return render(request, 'inventory/teacher_dashboard.html')

@login_required
def request_item(request):
    if request.method == 'POST':
        form = ItemRequestForm(request.POST)
        if form.is_valid():
            item_request = form.save(commit=False)
            item_request.requested_by = request.user
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

