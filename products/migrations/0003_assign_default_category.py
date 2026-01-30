from django.db import migrations


def create_default_category(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    Product = apps.get_model('products', 'Product')

    uncategorized, created = Category.objects.get_or_create(
        name='Uncategorized', defaults={'description': 'Default category for uncategorized products.'}
    )

    # Assign to existing products with null category
    Product.objects.filter(category__isnull=True).update(category=uncategorized)


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_team_product_products_pr_team_id_21af15_idx'),
    ]

    operations = [
        migrations.RunPython(create_default_category, reverse_code=migrations.RunPython.noop),
    ]
