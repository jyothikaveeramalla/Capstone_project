from decimal import Decimal
from django.test import TestCase, override_settings
from accounts.models import User
from artisans.models import ArtisanProfile
from products.models import Product


@override_settings(USD_TO_INR_RATE=83, MIN_PRICE_INR=500, MAX_PRICE_INR=5000)
class ProductModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="artisan_user", password="pass123", role="artisan", first_name="Art", last_name="San")
        self.artisan = ArtisanProfile.objects.create(
            user=self.user,
            craft_type='textiles',
            description='Test artisan',
            years_of_experience=1,
            workshop_location='Test'
        )

    def test_original_price_clamped_to_min_and_selling_computed(self):
        # original_price very low in USD -> should be clamped to MIN_INR / RATE
        p = Product(artisan=self.artisan, name='Small', description='desc', price=Decimal('1.00'), original_price=Decimal('1.00'), discount_percent=Decimal('10.00'), image='products/placeholder.jpg')
        p.save()

        min_usd = (Decimal('500') / Decimal('83')).quantize(Decimal('0.01'))
        self.assertEqual(p.original_price, min_usd)
        # When computed selling_price falls below MIN_INR it will be clamped to the min USD bound
        min_usd = (Decimal('500') / Decimal('83')).quantize(Decimal('0.01'))
        self.assertEqual(p.selling_price, min_usd)
        self.assertTrue(p.selling_price <= p.original_price)
        # legacy price synced
        self.assertEqual(p.price, p.selling_price)

    def test_discount_normalization_and_clamping(self):
        # Very large discount should normalize to 100 and selling_price gets clamped
        p = Product(artisan=self.artisan, name='HugeDisc', description='desc', price=Decimal('100.00'), original_price=Decimal('100.00'), discount_percent=Decimal('150.00'), image='products/placeholder.jpg')
        p.save()
        # discount_percent normalized to 100.00
        self.assertEqual(p.discount_percent, Decimal('100.00'))
        # selling_price computed -> 0.00 then clamped to min bound
        min_usd = (Decimal('500') / Decimal('83')).quantize(Decimal('0.01'))
        self.assertGreaterEqual(p.selling_price, min_usd)

    def test_legacy_price_fallback_and_rounding(self):
        # If original_price absent, fallback to legacy price
        p = Product(artisan=self.artisan, name='Legacy', description='desc', price=Decimal('20.00'), original_price=None, discount_percent=None, image='products/placeholder.jpg')
        p.save()
        self.assertEqual(p.original_price, Decimal('20.00'))
        # selling_price should fallback to price
        self.assertEqual(p.selling_price, Decimal('20.00'))

    def test_negative_discount_clamped_to_zero(self):
        p = Product(artisan=self.artisan, name='NegDisc', description='desc', price=Decimal('30.00'), original_price=Decimal('30.00'), discount_percent=Decimal('-5.00'), image='products/placeholder.jpg')
        p.save()
        self.assertEqual(p.discount_percent, Decimal('0.00'))
        # saving enforces selling < original, so selling becomes original - 0.01
        self.assertEqual(p.selling_price, Decimal('29.99'))
