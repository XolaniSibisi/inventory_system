from django.forms import ModelForm, ChoiceField, Select, Form
from .models import Invoice


class UpdateStatusForm(Form):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    new_status = ChoiceField(choices=STATUS_CHOICES, widget=Select(attrs={'class': 'form-control'}))

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'payment_method'
        ]

    def clean(self):
        cleaned_data = super().clean()
        payment_status = cleaned_data.get('payment_status')
        payment_due_date = cleaned_data.get('payment_due_date')

       
        if payment_status == 'paid' and not payment_due_date:
            self.add_error('payment_due_date', 'Payment due date is required for paid invoices.')


class uploadPaymentForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['payment_proof']
