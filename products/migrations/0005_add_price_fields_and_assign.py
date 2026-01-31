from django.db import migrations, models
from decimal import Decimal


def assign_prices(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    from django.conf import settings
    rate = Decimal(getattr(settings, 'USD_TO_INR_RATE', 83))
    min_inr = 500
    max_inr = 5000

    for p in Product.objects.all():
        # Deterministic varied original price based on id
        base = (p.id * 1237) % (max_inr - min_inr + 1)
        orig_inr = min_inr + base
        # Discount 5..40 deterministic
        disc = 5 + ((p.id * 97) % 36)
        # Compute selling INR
        selling_inr = int(Decimal(orig_inr) * (100 - Decimal(disc)) / Decimal(100))

        # Convert to USD and set fields
        orig_usd = (Decimal(orig_inr) / rate).quantize(Decimal('0.01'))
        sell_usd = (Decimal(selling_inr) / rate).quantize(Decimal('0.01'))

        p.original_price = orig_usd
        p.discount_percent = Decimal(disc)
        p.selling_price = sell_usd
        # Keep legacy price in sync
        p.price = p.selling_price
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_merge_20260131_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='original_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_percent',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='selling_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True),
        ),
        migrations.RunPython(assign_prices, reverse_code=migrations.RunPython.noop),
    ]