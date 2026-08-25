from django.test import TestCase
from django.urls import reverse

from .models import Movement, Product


class InventoryCrudTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Cuaderno', description='Cuaderno universitario', price='2500.00', stock=10
        )

    def test_product_crud_and_csrf_token(self):
        response = self.client.get(reverse('product_create'))
        self.assertContains(response, 'csrfmiddlewaretoken')
        response = self.client.post(reverse('product_create'), {
            'name': 'Lápiz', 'description': 'Grafito', 'price': '500.00', 'stock': 25,
        })
        self.assertRedirects(response, reverse('product_list'))
        pencil = Product.objects.get(name='Lápiz')
        response = self.client.post(reverse('product_update', args=[pencil.id]), {
            'name': 'Lápiz HB', 'description': 'Grafito', 'price': '600.00', 'stock': 20,
        })
        self.assertRedirects(response, reverse('product_list'))
        pencil.refresh_from_db()
        self.assertEqual(pencil.name, 'Lápiz HB')
        response = self.client.post(reverse('product_delete', args=[pencil.id]))
        self.assertRedirects(response, reverse('product_list'))
        self.assertFalse(Product.objects.filter(pk=pencil.id).exists())

    def test_movement_create_update_delete_adjusts_stock(self):
        response = self.client.post(reverse('movement_create'), {
            'product': self.product.id, 'movement_type': 'IN', 'quantity': 5,
        })
        self.assertRedirects(response, reverse('movement_list'))
        movement = Movement.objects.get()
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 15)
        response = self.client.post(reverse('movement_update', args=[movement.id]), {
            'product': self.product.id, 'movement_type': 'OUT', 'quantity': 3,
        })
        self.assertRedirects(response, reverse('movement_list'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 7)
        response = self.client.post(reverse('movement_delete', args=[movement.id]))
        self.assertRedirects(response, reverse('movement_list'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)

    def test_movement_rejects_negative_stock(self):
        response = self.client.post(reverse('movement_create'), {
            'product': self.product.id, 'movement_type': 'OUT', 'quantity': 11,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'stock en negativo')
        self.assertEqual(Movement.objects.count(), 0)

# Create your tests here.
