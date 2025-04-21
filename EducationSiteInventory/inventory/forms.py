from django import forms
from .models import ItemRequest
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ItemRequestForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = ['item', 'quantity_requested', 'reason']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')
