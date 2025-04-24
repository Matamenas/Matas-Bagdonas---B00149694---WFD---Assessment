from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group
from .models import CustomUser, Category, Item, ItemRequest

class InventoryTests(TestCase):
    def setUp(self):
        # Create groups
        Group.objects.create(name='teacher')
        Group.objects.create(name='inventory manager')

        # Create test user
        self.user = CustomUser.objects.create_user(username='testuser', password='pass1234', role='teacher')
        self.user.groups.add(Group.objects.get(name='teacher'))

        # Login client
        self.client = Client()
        self.client.login(username='testuser', password='pass1234')

        # Create category and item
        self.category = Category.objects.create(name="Stationery")
        self.item = Item.objects.create(name="Marker", category=self.category, quantity=10)

    def test_item_creation(self):
        response = self.client.get(reverse('item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Marker")

    def test_item_request_submission(self):
        response = self.client.post(reverse('request_item'), {
            'item': self.item.id,
            'quantity_requested': 2,
            'reason': 'For classroom use',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ItemRequest.objects.count(), 1)

    def test_request_approval_reduces_inventory(self):
        # Submit request
        item_request = ItemRequest.objects.create(
            item=self.item,
            quantity_requested=3,
            reason="Test",
            requested_by=self.user,
            teacher=self.user,
        )

        # Approve request
        response = self.client.get(reverse('approve_request', args=[item_request.id]))
        item_request.refresh_from_db()
        self.item.refresh_from_db()

        self.assertEqual(item_request.status, 'approved')
        self.assertEqual(self.item.quantity, 7)

    def test_reject_request_does_not_change_quantity(self):
        item_request = ItemRequest.objects.create(
            item=self.item,
            quantity_requested=5,
            reason="Test",
            requested_by=self.user,
            teacher=self.user,
        )

        self.client.get(reverse('reject_request', args=[item_request.id]))
        item_request.refresh_from_db()
        self.item.refresh_from_db()

        self.assertEqual(item_request.status, 'rejected')
        self.assertEqual(self.item.quantity, 10)
