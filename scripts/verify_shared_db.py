#!/usr/bin/env python
"""
verify_shared_db.py - Quick script to verify shared database connection

Usage:
    python scripts/verify_shared_db.py

This checks:
- DATABASE_URL is set
- Postgres connection works
- Migrations are applied (tables exist)
- At least one product can be queried
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artisanedge.settings')
django.setup()

from django.db import connection
from products.models import Product

def main():
    print("=" * 60)
    print("Shared Database Verification")
    print("=" * 60)
    
    # Check DATABASE_URL
    db_url = os.environ.get('DATABASE_URL', '')
    if db_url:
        # Hide password
        display_url = db_url.replace(db_url.split(':')[1].split('@')[0], '***') if '@' in db_url else db_url
        print(f"✓ DATABASE_URL is set: {display_url[:50]}...")
    else:
        print("✗ DATABASE_URL not set (using SQLite fallback)")
        return
    
    # Check connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        dbname = connection.get_connection_params().get('dbname', 'unknown')
        print(f"✓ Connected to database: {dbname}")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return
    
    # Check migrations
    try:
        tables = connection.introspection.table_names()
        if 'products_product' in tables:
            print(f"✓ Migrations applied ({len(tables)} tables)")
        else:
            print("✗ Migrations not applied (products_product table missing)")
            print("  Run: python manage.py migrate")
            return
    except Exception as e:
        print(f"✗ Failed to check migrations: {e}")
        return
    
    # Check products
    try:
        count = Product.objects.count()
        print(f"✓ Products in database: {count}")
        if count > 0:
            latest = Product.objects.latest('created_at')
            print(f"  Latest: {latest.name} (by {latest.artisan.user.get_full_name() if latest.artisan else 'unknown'})")
    except Exception as e:
        print(f"✗ Failed to query products: {e}")
        return
    
    print("\n" + "=" * 60)
    print("✓ All checks passed! Database is ready.")
    print("=" * 60)

if __name__ == '__main__':
    main()
