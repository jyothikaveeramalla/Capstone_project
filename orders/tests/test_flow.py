from django.test import TestCase, Client, override_settings
from django.urls import reverse
from accounts.models import User
from artisans.models import ArtisanProfile
from products.models import Product
from cart.models import Cart, CartItem
from decimal import Decimal


@override_settings(USD_TO_INR_RATE=83, MIN_PRICE_INR=500, MAX_PRICE_INR=5000)
class ShippingFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='buyer3', password='pass123', role='customer')
        self.artisan_user = User.objects.create_user(username='artisan3', password='pass123', role='artisan')
        self.artisan = ArtisanProfile.objects.create(
            user=self.artisan_user,
            craft_type='textiles',
            description='desc',
            years_of_experience=3,
            workshop_location='Somewhere'
        )
        self.client.login(username='buyer3', password='pass123')
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_page_has_proceed_to_shipping(self):
        p = Product.objects.create(
            artisan=self.artisan,
            name='FlowProd',
            description='desc',
            price=Decimal('20.00'),
            original_price=Decimal('20.00'),
            discount_percent=Decimal('0.00'),
            image='products/placeholder.jpg'
        )
        CartItem.objects.create(cart=self.cart, product=p, quantity=1)

        resp = self.client.get(reverse('cart'))
        self.assertContains(resp, reverse('shipping'))

    def test_shipping_post_redirects_to_checkout_and_persists(self):
        # Add a cart item so checkout is reachable
        p = Product.objects.create(
            artisan=self.artisan,
            name='FlowProd2',
            description='desc',
            price=Decimal('20.00'),
            original_price=Decimal('20.00'),
            discount_percent=Decimal('0.00'),
            image='products/placeholder.jpg'
        )
        CartItem.objects.create(cart=self.cart, product=p, quantity=1)

        data = {
            'full_name': 'Flow Buyer',
            'email': 'flow@example.com',
            'phone': '9999999999',
            'address': '1 Flow St',
            'city': 'City',
            'state': 'State',
            'pincode': '000000'
        }
        resp = self.client.post(reverse('shipping'), data=data, follow=True)
        self.assertRedirects(resp, reverse('checkout'))
        # Confirm session has shipping data
        session = self.client.session
        self.assertIn('shipping', session)
        self.assertEqual(session['shipping']['full_name'], 'Flow Buyer')

    def test_checkout_without_shipping_redirects(self):
        # Add a cart item so checkout is reachable
        p = Product.objects.create(
            artisan=self.artisan,
            name='FlowProd3',
            description='desc',
            price=Decimal('20.00'),
            original_price=Decimal('20.00'),
            discount_percent=Decimal('0.00'),
            image='products/placeholder.jpg'
        )
        CartItem.objects.create(cart=self.cart, product=p, quantity=1)

        # Ensure checkout redirects to shipping if no session
        resp = self.client.get(reverse('checkout'), follow=True)
        self.assertRedirects(resp, reverse('shipping'))
