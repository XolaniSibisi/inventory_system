# Generated by Django 5.0.3 on 2024-06-01 18:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='accountantPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('view_records', 'Manage records'), ('add_record', 'Add record'), ('update_record', 'Update records')),
            },
        ),
        migrations.CreateModel(
            name='CustomerPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('view_cart', 'Can view cart'), ('add_to_cart', 'Can add items to cart'), ('remove_from_cart', 'Can remove items from cart'), ('update_cart', 'Can update cart'), ('clear_cart', 'Can clear cart'), ('checkout', 'Can proceed to checkout'), ('view_order_history', 'Can view order history'), ('view_product_details', 'Can view product details')),
            },
        ),
        migrations.CreateModel(
            name='Distributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact', models.TextField()),
                ('email', models.TextField()),
                ('area', models.CharField(blank=True, max_length=200, null=True)),
                ('delivery_schedule', models.CharField(max_length=200)),
                ('types_of_food', models.CharField(max_length=200)),
                ('delivery_vehicles', models.CharField(max_length=200)),
                ('delivery_process', models.TextField()),
                ('minimum_order_requirements', models.CharField(max_length=100)),
                ('delivery_fees', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StaffPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('view_dashboard', 'Can view dashboard'), ('manage_products', 'Can manage products'), ('view_products', 'Manage products')),
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('subscribed_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('receive_marketing_emails', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SupplierPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('view_inventory', 'Manage inventory'), ('view_products', 'Manage products'), ('manage_orders', 'Can manage orders'), ('add_products', 'Add products to inventory')),
            },
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_deleted', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=200)),
                ('catalog_file', models.FileField(blank=True, null=True, upload_to='uploaded_catalogs/')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cost_per_item', models.DecimalField(decimal_places=2, max_digits=19)),
                ('quantity_in_stock', models.IntegerField()),
                ('quantity_sold', models.IntegerField(default=0)),
                ('sales', models.DecimalField(decimal_places=2, max_digits=19)),
                ('stock_date', models.DateField(auto_now_add=True)),
                ('last_sales_date', models.DateField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('barcode', models.ImageField(blank=True, null=True, upload_to='barcodes/')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('sales_data', models.JSONField(blank=True, null=True)),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.catalog')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')])),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.inventory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SalesData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('quantity_sold', models.IntegerField()),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='accounts.inventory')),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('inventory', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='accounts.inventory')),
            ],
        ),
    ]
