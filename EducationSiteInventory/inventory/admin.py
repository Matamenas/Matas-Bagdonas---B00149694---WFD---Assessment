from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Item, ItemRequest
from .models import Category

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active", "groups"]
    search_fields = ["username", "email"]
    ordering = ["username"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ['name', 'category', 'quantity']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(ItemRequest)
class ItemRequestAdmin(admin.ModelAdmin):
    model = ItemRequest
    list_display = ['item', 'quantity_requested', 'status', 'reason']
    list_filter = ['status', 'reason']
    search_fields = ['item']
    ordering = ['status']

