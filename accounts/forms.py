from django import forms
from django.forms import ModelForm, ChoiceField, Select, Form
from .models import Catalog, Inventory, Order, Subscriber, Distributor, Testimonial
from orders.models import Invoice

class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ['name', 'description']

class uploadCatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ['name', 'description', 'catalog_file']

class InventoryForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['catalog'].queryset = Catalog.objects.filter(supplier=user)

    class Meta:
        model = Inventory
        fields = ['catalog', 'name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold', 'image']

    # Define a hidden field for catalog_id
    # catalog_id = forms.IntegerField(widget=forms.HiddenInput())

class InventoryUpdateForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ["name", "cost_per_item", "quantity_in_stock", "quantity_sold", "image"]


class AddInventoryForm(ModelForm):
    barcode = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Barcode'}))
    image = forms.ImageField(required=False)

    class Meta:
        model = Inventory
        fields = ["name", "cost_per_item", "quantity_in_stock", "quantity_sold", "barcode", "image"]

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'customer','quantity_ordered']

class UpdateStatusForm(Form):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    new_status = ChoiceField(choices=STATUS_CHOICES, widget=Select(attrs={'class': 'form-control'}))

class UserInputForm(forms.Form):
    user_input = forms.CharField(label='user_name', max_length=100)

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'billing_address',
            'payment_method',
            'notes',
        ]

    def clean(self):
        cleaned_data = super().clean()
        payment_status = cleaned_data.get('payment_status')
        payment_due_date = cleaned_data.get('payment_due_date')

       
        if payment_status == 'paid' and not payment_due_date:
            self.add_error('payment_due_date', 'Payment due date is required for paid invoices.')

class SalesDataUploadForm(forms.Form):
    sales_data = forms.FileField()

class SubscriptionForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    class Meta:
        model = Subscriber
        fields = ['email']

class BulkEmailForm(forms.Form):
    RECIPIENT_CHOICES = [
        ('all', 'All Users'),
        ('active', 'Active Users'),
        ('inactive', 'Inactive Users'),
    ]
    
    recipient_type = forms.ChoiceField(choices=RECIPIENT_CHOICES, label='Recipient Type')
    subject = forms.CharField(max_length=100, label='Subject')
    message = forms.CharField(widget=forms.Textarea, label='Message')
    file = forms.FileField(label='Upload File', required=False)


class DistributorForm(forms.ModelForm):
    class Meta:
        model = Distributor
        fields = '__all__'

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['text', 'rating']

class SearchForm(forms.Form):
    address = forms.CharField(label='Enter your address', max_length=100)


