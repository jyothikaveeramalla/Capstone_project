from decimal import Decimal
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from accounts.models import User
from artisans.models import ArtisanProfile
from products.models import Product
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem


@override_settings(USD_TO_INR_RATE=83, MIN_PRICE_INR=500, MAX_PRICE_INR=5000)
class CheckoutTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='buyer2', password='pass123', role='customer')
        self.artisan_user = User.objects.create_user(username='artisan2', password='pass123', role='artisan')
        self.artisan = ArtisanProfile.objects.create(
            user=self.artisan_user,
            craft_type='textiles',
            description='desc',
            years_of_experience=3,
            workshop_location='Somewhere'
        )
        self.client.login(username='buyer2', password='pass123')
        self.cart = Cart.objects.create(user=self.user)

    def test_checkout_sets_orderitem_price_to_selling_price(self):
        p = Product.objects.create(
            artisan=self.artisan,
            name='CheckoutProd',
            description='desc',
            price=Decimal('100.00'),
            original_price=Decimal('100.00'),
            discount_percent=Decimal('10.00'),
            quantity_in_stock=5,
            image='products/placeholder.jpg'
        )
        p.save()
        # Original price is clamped to MAX_INR/USD bounds; selling price reflects that clamp + discount
        max_usd = (Decimal('5000') / Decimal('83')).quantize(Decimal('0.01'))
        expected_sp = (max_usd * (Decimal('100') - Decimal('10')) / Decimal('100')).quantize(Decimal('0.01'))
        self.assertEqual(p.selling_price, expected_sp)

        CartItem.objects.create(cart=self.cart, product=p, quantity=1)

        # First submit shipping info
        resp = self.client.post(reverse('shipping'), data={
            'full_name': 'Buyer Name',
            'email': 'buyer@example.com',
            'phone': '9999999999',
            'address': '123 Test St',
            'city': 'City',
            'state': 'State',
            'pincode': '123456'
        }, follow=True)
        self.assertRedirects(resp, reverse('checkout'))

        # Then place the order (checkout uses shipping from session)
        response = self.client.post(reverse('checkout'), follow=True)

        # Find the created order
        order = Order.objects.filter(customer=self.user).first()
        self.assertIsNotNone(order)
        order_item = order.items.first()
        self.assertIsNotNone(order_item)
        self.assertEqual(order_item.product_price, p.selling_price)
        self.assertEqual(order.subtotal, p.selling_price)
        # shipping cost should be included in total
        shipping_inr = Decimal(50)
        shipping_usd = (shipping_inr / Decimal(83)).quantize(Decimal('0.01'))
        self.assertEqual(order.shipping_cost, shipping_usd)
        self.assertEqual(order.total_amount, p.selling_price + shipping_usd)
