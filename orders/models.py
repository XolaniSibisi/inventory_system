from django.db import models

# Create your models here.
class cart(models.Model):
    item = models.CharField(max_length=100, null=False, blank=False)
    cost_per_item = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    total_amount = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    customer = models.CharField(max_length=100, default="")
    catalog = models.IntegerField(null=True, blank=False)
    

    def __str__(self) -> str:
        return self.item
    
class OrderAmount(models.Model):
    amount_due = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    customer = models.CharField(max_length=100, default="")
    cart_count = models.IntegerField(null=True, blank=False)

    def __str__(self) -> str:
        return str(self.amount_due)
    

class customerOrderHistory(models.Model):

    order_id = models.CharField(max_length=100, default="")
    order_date = models.DateTimeField(auto_now_add=True)
    customer = models.CharField(max_length=100, default="")
    product = models.CharField(max_length=100, default="")
    quantity_ordered = models.PositiveIntegerField(null=True)
    amount_spent = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    customer_order_status = models.CharField(max_length=100, default='pending', null=True)
    payment_method = models.CharField(max_length=100, default="")
    payment_status = models.CharField(max_length=100, default="")
    catalog = models.IntegerField(null=True, blank=False)

    def __str__(self) -> str:
        return str(self.order_id)
    
class cart_records(models.Model):

    item = models.CharField(max_length=100, null=False, blank=False)
    cost_per_item = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    total_amount = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=False)
    customer = models.CharField(max_length=100, default="")
    
    def __str__(self) -> str:
        return str(self.item)
    
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    order_id = models.CharField(max_length=100, default="")
    order_date = models.DateTimeField(auto_now_add=True)
    customer = models.CharField(max_length=100, default="")
    product = models.CharField(max_length=100, default="")
    quantity_ordered = models.PositiveIntegerField(null=True)
    amount_spent = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=100, default="")
    payment_status = models.CharField(max_length=100, default="")
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    supplier = models.CharField(max_length=100, default="")
    catalog = models.IntegerField(null=True, blank=False)
    supplier_email = models.EmailField(null=True)

    def __str__(self):
        return f"Order #{self.id}- {self.order_id} - {self.product} - {self.customer} - {self.quantity_ordered} units - Status: {self.order_status}"
    
class Invoice(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
    ]

    PAYMENT_METHOD_CHOICES =[
        ('Debit/Credit card', 'Debit/Credit Card'),
        ('Cash Deposit', 'Cash Deposit')
    ]

    invoice_no = models.CharField(max_length=255, default="")
    order = models.CharField(max_length=255, default="")
    date_created = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    billing_name = models.CharField(max_length=255)
    billing_address = models.TextField(null=True, blank=True)
    billing_email = models.EmailField()

    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='')
    payment_due_date = models.DateField(blank=True, null=True)
    payment_proof = models.FileField(upload_to='payment_proof/', null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)

    supplier_info = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Invoice #{self.pk}"
    
