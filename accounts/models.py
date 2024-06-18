# accounts/models.py
from django.db import models
from orders.models import Order
from django.contrib.auth.models import User

class Catalog(models.Model):
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    description = models.CharField(max_length=200)
    catalog_file = models.FileField(upload_to='uploaded_catalogs/', null=True, blank=True)
    supplier = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Inventory(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    cost_per_item = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    quantity_in_stock = models.IntegerField(null=False, blank=False)
    quantity_sold = models.IntegerField(null=False, blank=False, default=0)
    sales = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    stock_date = models.DateField(auto_now_add=True)
    last_sales_date = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    barcode = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    # New field to store historical sales data
    sales_data = models.JSONField(null=True, blank=True)

    def update_sales_data(self):
        # Fetch historical sales records for this inventory item
        historical_sales = Order.objects.filter(product=self).exclude(
            order_status='pending').order_by('order_date')

        # Update the sales_data dictionary
        sales_data = {
            'date': [record.order_date.strftime('%Y-%m-%d') for record in historical_sales],
            'quantity_sold': [record.quantity_ordered for record in historical_sales],
        }

        # Save the updated sales_data
        self.sales_data = sales_data
        self.save()

    def __str__(self) -> str:
        return self.name

# Create your models here.


class CustomerPermissions(models.Model):
    class Meta:
        permissions = (
            ("view_cart", "Can view cart"),
            ("add_to_cart", "Can add items to cart"),
            ("remove_from_cart", "Can remove items from cart"),
            ("update_cart", "Can update cart"),
            ("clear_cart", "Can clear cart"),
            ("checkout", "Can proceed to checkout"),
            ("view_order_history", "Can view order history"),
            ("view_product_details", "Can view product details"),
        )


class StaffPermissions(models.Model):
    class Meta:
        permissions = (
            ("view_dashboard", "Can view dashboard"),
            ("manage_products", "Can manage products"),
            ("view_products", "Manage products"),
            # ("view_inventory", "Manage inventory")
            # Add more permissions as needed
        )


class SupplierPermissions(models.Model):
    class Meta:
        permissions = (
            ("view_inventory", "Manage inventory"),
            ("view_products", "Manage products"),
            ("manage_orders", "Can manage orders"),
            ("add_products", "Add products to inventory")
            # Add more permissions as needed
        )

class accountantPermissions(models.Model):
  
    class Meta:
        permissions = (
            ("view_records", "Manage records"),
            ("add_record", "Add record"),
            ("update_record", "Update records"),
            # Add more permissions as needed
        )


class SalesData(models.Model):
    product = models.ForeignKey(
    Inventory, on_delete=models.CASCADE, default=None)
    date = models.DateField()
    quantity_sold = models.IntegerField()


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    receive_marketing_emails = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    
class Rating(models.Model):
    RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    )

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)

class Testimonial(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, default=None)  # ForeignKey relationship
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text

class Distributor(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    area = models.CharField(max_length=200, null=True, blank=True)
    delivery_schedule = models.CharField(max_length=200)
    types_of_food = models.CharField(max_length=200)
    delivery_vehicles = models.CharField(max_length=200)
    delivery_process = models.TextField()
    minimum_order_requirements = models.CharField(max_length=100)
    delivery_fees = models.CharField(max_length=100)

    def __str__(self):
        return self.name
