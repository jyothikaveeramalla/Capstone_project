from django.db import migrations
from decimal import Decimal


def clamp_prices(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    from django.conf import settings
    rate = Decimal(getattr(settings, 'USD_TO_INR_RATE', 83))
    min_inr = Decimal(getattr(settings, 'MIN_PRICE_INR', 500))
    max_inr = Decimal(getattr(settings, 'MAX_PRICE_INR', 5000))

    min_usd = (min_inr / rate).quantize(Decimal('0.01'))
    max_usd = (max_inr / rate).quantize(Decimal('0.01'))

    for p in Product.objects.all():
        changed = False
        if p.price is not None:
            if p.price < min_usd:
                p.price = min_usd
                changed = True
            elif p.price > max_usd:
                p.price = max_usd
                changed = True
        if p.cost_price:
            if p.cost_price < min_usd:
                p.cost_price = min_usd
                changed = True
            elif p.cost_price > max_usd:
                p.cost_price = max_usd
                changed = True
            if p.cost_price > p.price:
                p.cost_price = p.price
                changed = True
        if changed:
            p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(clamp_prices, reverse_code=migrations.RunPython.noop),
    ]
