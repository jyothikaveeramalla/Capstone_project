from decimal import Decimal
from django.test import TestCase, override_settings
from accounts.models import User
from artisans.models import ArtisanProfile
from products.models import Product
from cart.models import Cart, CartItem


@override_settings(USD_TO_INR_RATE=83, MIN_PRICE_INR=500, MAX_PRICE_INR=5000)
class CartPricingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='pass123', role='customer')
        self.artisan_user = User.objects.create_user(username='artisan', password='pass123', role='artisan', first_name='A')
        self.artisan = ArtisanProfile.objects.create(
            user=self.artisan_user,
            craft_type='textiles',
            description='desc',
            years_of_experience=2,
            workshop_location='Nowhere'
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_total_uses_selling_price(self):
        p = Product.objects.create(
            artisan=self.artisan,
            name='Prod1',
            description='desc',
            price=Decimal('50.00'),
            original_price=Decimal('50.00'),
            discount_percent=Decimal('20.00'),
            image='products/placeholder.jpg'
        )
        p.save()
        # selling 40.00
        self.assertEqual(p.selling_price, Decimal('40.00'))
        CartItem.objects.create(cart=self.cart, product=p, quantity=2)
        self.assertEqual(self.cart.get_total_price(), p.selling_price * 2)
