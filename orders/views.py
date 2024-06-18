from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from accounts.models import Inventory, Catalog
from .models import Order, Invoice , cart, OrderAmount, customerOrderHistory, cart_records
from user.models import Profile
from django.shortcuts import get_object_or_404
from .forms import UpdateStatusForm, InvoiceForm, uploadPaymentForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
import uuid
from datetime import datetime, timedelta
from django.db.models import Sum
from xhtml2pdf import pisa
from django.template.loader import get_template
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import User


#adding items to cart for customers
@login_required
def view_cart(request):
    logged_user = request.user
    cart_items = cart.objects.filter(customer=logged_user)
    amount = OrderAmount.objects.filter(customer=logged_user)

    return render(request, 'orders/cart.html', {'items': cart_items, 'amount': amount})

@login_required
def add_to_cart(request, item_id):
    
    #before placing another order, clear the temporary hold of cart_record
    cart_record = cart_records.objects.all()
    cart_record.delete()
    
    #add items to cart
    item = get_object_or_404(Inventory, id=item_id)
    if item.quantity_in_stock <= 0:
        messages.warning(request, "Item out of stock!")
        return redirect("products")
    else:
        item_name = item.name
        item_cost = item.cost_per_item
        quantities = 1
        logged_user = request.user
        catalog = item.catalog_id
    
    # only allow placement from one catalog
    current_cart_item = cart.objects.filter(customer=logged_user)

    if current_cart_item.last() == None or current_cart_item.last().catalog == catalog:

        user_specific_items = cart.objects.filter(customer=logged_user, item=item_name)
        if user_specific_items.exists():
            item = user_specific_items.first()
        
            #increase quantity
            new_quantity=item.quantity
            new_quantity = new_quantity + 1
            item.quantity = new_quantity

            #increase total_amount
            price = item.cost_per_item
            new_amount = item.total_amount
            new_amount = new_amount + price
            item.total_amount = new_amount
            item.save()

        else:
            new_entry = cart(item = item_name, cost_per_item = item_cost, quantity=quantities, total_amount=item_cost, customer=logged_user, catalog=catalog)
            new_entry.save()

    # Retrieve all instances of OrderAmount
        existing_amounts = OrderAmount.objects.filter(customer=logged_user)

        if existing_amounts.exists():
            existing_amount = existing_amounts.first()

            existing_amount.amount_due += item_cost      # order amount
            existing_amount.cart_count += 1              # cart count  
            existing_amount.save()
        else:
            # If no instances exist, create a new one
            new_price = OrderAmount(amount_due=item_cost, customer=logged_user, cart_count=quantities)
            new_price.save()

        #badge cart count
        cart_record = OrderAmount.objects.get(customer=logged_user)
        request.session['cart_count'] = cart_record.cart_count
        print(cart_record.cart_count)
        
        messages.success(request, "Item added to cart")

    else:
        messages.warning(request, "Items from one catalog allowed per order!")
    return redirect("products")

@login_required
def delete_from_cart(request, item_id):
    #remove from cart
    item = get_object_or_404(cart, id=item_id)
    item_cost = item.total_amount
    item_quantity = item.quantity
    logged_user = request.user
    
    existing_amount =OrderAmount.objects.get(customer=logged_user)
    existing_amount.amount_due -= item_cost     #decrease total price
    existing_amount.cart_count -= item_quantity #decrease cart count
    
    item.delete()
    existing_amount.save()

    request.session['cart_count'] = existing_amount.cart_count
    
    if existing_amount.amount_due <= 0:
        existing_amount.delete()

    messages.success(request, "Item removed from cart")
    return redirect('view_cart')

@login_required
def increase_cart_quantity(request, item_id):
    item = get_object_or_404(cart, id=item_id)
    
    #increase quantity
    new_quantity=item.quantity
    new_quantity = new_quantity + 1
    item.quantity = new_quantity

    #increase total_amount
    price = item.cost_per_item
    new_amount = item.total_amount
    new_amount = new_amount + price
    item.total_amount = new_amount

    item.save()

    #increase total price
    logged_user = request.user
    existing_amount = OrderAmount.objects.get(customer=logged_user)
    existing_amount.amount_due += price
    existing_amount.cart_count += 1
    existing_amount.save()
    
    request.session['cart_count'] = existing_amount.cart_count
    return redirect("view_cart")

@login_required
def decrease_cart_quantity(request, item_id):
    item = get_object_or_404(cart, id=item_id)
    logged_user = request.user
    existing_amount = OrderAmount.objects.get(customer=logged_user)
    
    new_quantity=item.quantity
    new_amount = item.total_amount
    price = item.cost_per_item

    if new_quantity > 0 and new_amount > 0  and existing_amount.amount_due > 0:
        #decrease quantity
        new_quantity = new_quantity - 1
        item.quantity = new_quantity

        #decrease price
        new_amount = new_amount - price
        item.total_amount = new_amount

        #decrease total price
        existing_amount.amount_due -= price
        existing_amount.cart_count -= 1 

        item.save()
        existing_amount.save()

        #count items in cart
        request.session['cart_count'] = existing_amount.cart_count
    
    else:
        pass

    if new_quantity < 1:
        item.delete()
    else: 
        pass
    
    if existing_amount.amount_due <= 0:
        existing_amount.delete()

    return redirect("view_cart")

@login_required
def delete_cart(request):
    logged_user = request.user
    cart_entry = cart.objects.filter(customer=logged_user)
    cart_entry.delete()

    
    cart_amount = OrderAmount.objects.filter(customer=logged_user)
    cart_amount.delete()

    messages.success(request, "Cart cleared!")
    request.session['cart_count'] = 0
    return redirect("view_cart")


#Order management
@login_required
def order_list(request):
    logged_supplier = request.user.first_name
    order_lists = Order.objects.filter(supplier=logged_supplier)
    return render(request, 'orders/order_list.html', {'orders': order_lists, 'supplier': logged_supplier})


@login_required
def update_order_status(request, order_id):

    #block order status once it is changed to delivered
    order = get_object_or_404(Order, id=order_id)
    invoice = get_object_or_404(Invoice, order=order.order_id)

    customer_order = get_object_or_404(customerOrderHistory, order_id=order.order_id)
    completion_status = order.order_status 

    if completion_status == "delivered" or completion_status =="Order canceled":
        messages.warning(request, "Cannot update on status on a complete or canceled order!")
        return redirect("order_list")
    else:
        if request.method == 'POST':
            form = UpdateStatusForm(request.POST)
                    
            if form.is_valid():
                pay_status = order.payment_status
            
                if pay_status == 'Paid':
                    #update orderlist status
                    new_status = form.cleaned_data['new_status']
                    order.order_status = new_status
                    order.save()

                    #update customer order status 
                    if new_status == 'shipped':
                        customer_order.customer_order_status = 'shipped'
                    elif new_status == 'approved':
                        customer_order.customer_order_status = 'approved'
                    elif new_status == 'delivered':
                        customer_order.customer_order_status = 'delivered'
                    
                    customer_order.save()

                    # Generate update emails
                    status = ""
                    if new_status == "pending":
                        status = ' is currently being processed'
                    elif new_status == "shipped":
                        status = ' has been shipped'
                    elif new_status == "approved":
                        status = 'is approved'
                    else:
                        status = "is delivered"

                    name = invoice.billing_name
                    email_address = invoice.billing_email
                    sender_email = settings.EMAIL_HOST_USER
                    email_body = f"""
                    Hello, {name}!

                    Thank you for placing your order with FarmFresh.

                    Please note that your order {status}.
                    

                    Best regards,
                    FarmFresh
                    """
                    # Create an EmailMessage object
                    email = EmailMessage(
                    'Order status update',
                    email_body,
                    sender_email,
                    [email_address],
                    )

                    # Send the email
                    email.send()
                    messages.success(request, "Order status updated!")
                # Redirect in both cases
                return redirect('order_list')
                
        else:
            form = UpdateStatusForm()

        return render(request, 'orders/update_status.html', {'form': form, 'order': order})
    
@login_required
def order_history(request):
    logged_user = request.user
    has_data = customerOrderHistory.objects.exists()
    if has_data:
        previous_orders = customerOrderHistory.objects.filter(customer=logged_user)
    else:
        previous_orders = customerOrderHistory.objects.all()
    return render(request, 'orders/order_history.html', {'orders': previous_orders, "user": logged_user})

@login_required
def return_order(request, order_id):
    logged_user = request.user
    current_order = customerOrderHistory.objects.filter(customer=logged_user).get(id=order_id)
    last_order = customerOrderHistory.objects.filter(customer=logged_user).last()
    if current_order == last_order:
        if current_order.customer_order_status != "Order canceled":

            if order_history:
                
                # Sum up items by name
                item_quantities = cart_records.objects.values('item').annotate(each_item_quantity=Sum('quantity'))
                print(item_quantities)

                #add each product back into the inventory
                for item in item_quantities:
                    item_name = item['item']
                    returning_quantity = item['each_item_quantity']
                    inventory_product = get_object_or_404(Inventory, name=item_name, catalog_id=current_order.catalog)
                    print(inventory_product)
                    ajusted_quantity = inventory_product.quantity_in_stock + returning_quantity
                    inventory_product.quantity_in_stock = ajusted_quantity

                    quantity_sold = inventory_product.quantity_sold
                    inventory_product.quantity_sold = max(0, quantity_sold - returning_quantity)
                    inventory_product.sales = float(inventory_product.cost_per_item) * float(inventory_product.quantity_sold)
                    inventory_product.save()

                #fetch product from order history and inventory and update their statuses
                returning_orderlist = get_object_or_404(Order, order_id=current_order.order_id)
                returning_orderlist.order_status = "Order canceled"
                current_order.customer_order_status = "Order canceled"
               
                # Change payment status on invoice, order and customer order history if its paid
                invoice = get_object_or_404(Invoice, order=current_order.order_id)

                refund = "Refund"
                no_refund = "Not eligible for refund"
                if current_order.payment_status == "Paid":
                    invoice.payment_status = refund
                    current_order.payment_status = refund
                    returning_orderlist.payment_status = refund

                elif current_order.payment_status == "Pending":
                    invoice.payment_status = no_refund
                    current_order.payment_status = no_refund
                    returning_orderlist.payment_status = no_refund
                
                returning_orderlist.save() 
                current_order.save()
                invoice.save()

                # Update supplier when an order has been canceled.
                name = returning_orderlist.supplier
                customer = invoice.billing_name
                subject = f"Order canceled - id#{invoice.order}!"
                email_address = returning_orderlist.supplier_email
                sender_email = settings.EMAIL_HOST_USER
                email_body = f"""
                            Hello, {name}

                            Please note that order #{invoice.order} has been canceled by {customer}.
                            Ensure to facilitate the refund process where applicable.

                            Best regards,
                            FarmFresh
                            """
                # Create an EmailMessage object
                email = EmailMessage(
                    subject,
                    email_body,
                    sender_email,
                    [email_address],
                    )

                # Send the email
                email.send()


                # Update customer for successful order return
                customer_name = invoice.billing_name
                customer_email = invoice.billing_email
                customer_subject = f"Order canceled - id#{invoice.order}!"
                email_message = f"""
                    Hello, {customer_name}!

                    Please note that your order has been successfully canceled.
                    

                    Best regards,
                    FarmFresh
                    """
                    # Create an EmailMessage object
                email_to_be_sent = EmailMessage(
                    customer_subject,
                    email_message,
                    sender_email,
                    [customer_email],
                    )

                # Send the email
                email_to_be_sent.send()

                print(f"from order: {returning_orderlist.order_id}- {returning_orderlist.payment_status}, from customer_order:{current_order.order_id}-{current_order.payment_status}, from invoice: {invoice.order}-{invoice.payment_status}- {invoice.id}")
                messages.success(request, "Order canceled!")
                
        else:
            pass
    else:
        pass
    return redirect('order_history')

login_required
def order_details(request):
    logged_user = request.user
    #initialise status
    status = "delivered"
    if customerOrderHistory.objects.filter(customer=logged_user).exists():
        previous_order =  customerOrderHistory.objects.filter(customer=logged_user).last()
        status = previous_order.customer_order_status
    else:
        pass

    if status == "delivered" or status == "Order canceled":
        #fetch required information
        #address, payment method and deliver notes placeholder
        address= "*******************"
        method = "*******************"
        notes = "*******************************************************************************"

        
        #billing name
        customer_name = f"{logged_user.first_name} {logged_user.last_name}"
        
        #Address
        if Profile.objects.filter(user_id=logged_user.id).exists():
            address = get_object_or_404(Profile, user_id=logged_user.id).address
            print(address)

        #invoice unique id
        prefix = logged_user
        random_part = uuid.uuid4().hex[:5].upper()
        invoice_id = f'{prefix}-{random_part}'
        
        #billing email
        email = request.user.email

        #payment date
        due_date = datetime.now().date() + timedelta(days=7)

        #Amount due
        order_amount = OrderAmount.objects.get(customer=logged_user)
        payment_amount = order_amount.amount_due

        # Create new invoice
        invoice = Invoice(invoice_no=invoice_id,
                        order=invoice_id, 
                        billing_name=customer_name, 
                        billing_email=email, 
                        payment_due_date=due_date, 
                        total_amount=payment_amount,
                        billing_address=address,
                        payment_method=method,
                        notes=notes
                        )

        invoice.save()
        #save cart entries before clearing
        existing_cart = cart.objects.filter(customer=logged_user)

        for item in existing_cart:
                item_name = item.item
                item_cost = item.cost_per_item
                item_quantity = item.quantity
                price = item.total_amount

                cart_record = cart_records(
                    item = item_name,
                    cost_per_item =item_cost,
                    quantity=item_quantity,
                    total_amount=price,
                    customer = logged_user
                )
                cart_record.save()
        pk=Invoice.objects.all().last().id
        return redirect('edit_invoice', pk)
    else:
        messages.warning(request, "Placing new order while one is in progress is not allowed!")
        return redirect("products")

@login_required
def invoice_detail(request):
    invoice = Invoice.objects.all().last()
    logged_user = request.user
    cart_items = cart_records.objects.filter(customer=logged_user)
    orderCount = OrderAmount.objects.all().last()
    context = {'invoice': invoice,
               'cart_items': cart_items,
               'orderCount': orderCount
               }
    
    return render(request, 'orders/invoice_detail.html', context)

@login_required
def edit_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('invoice_detail')
    else:
        form = InvoiceForm(instance=invoice)

    context = {'form': form, 'invoice': invoice}
    return render(request, 'orders/edit_invoice.html', context)

@login_required
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    logged_user = request.user
    cart_entry = cart.objects.filter(customer=logged_user)
    cart_entry.delete()

    order_amount = OrderAmount.objects.filter(customer=logged_user)
    order_amount.delete()
    request.session['cart_count'] = 0
    
    messages.success(request, "Order canceled")
    return redirect('products')

#generate pdf of invoice
@login_required
def invoice_pdf(request, pk):
     # Your data to be passed to the template
    invoice = get_object_or_404(Invoice, pk=pk)
    logged_user = request.user
    cart_items = cart_records.objects.filter(customer=logged_user)
    orderCount = OrderAmount.objects.all().last()
    context = {
    'invoice_number': invoice.invoice_no,
    'order_id': invoice.order,
    'total_amount': f"R{invoice.total_amount}",
    'date': invoice.date_created,
    'billing_name': invoice.billing_name,
    'billing_address': invoice.billing_address,
    'billing_email': invoice.billing_email,
    'payment_status': invoice.payment_status,
    'payment_method': invoice.payment_method,
    'due_date': invoice.payment_due_date,
    'notes': invoice.notes,
    'total_quantities': orderCount.cart_count,
    'order_items': [
        {
            'No': cart_item.id,
            'item': cart_item.item,
            'item_quantity': cart_item.quantity,
            'item_cost': cart_item.cost_per_item,
            'price': cart_item.total_amount
        }
        for cart_item in cart_items  # Assuming cart_records is a queryset or list of items
    ]
    # Add other data as needed
}
    #render the template
    template_path = 'orders/invoice_pdf.html'
    template = get_template(template_path)
    html = template.render(context)

     # Create the PDF
    response = HttpResponse(content_type='application/pdf')

    # Generate the PDF content using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Could not generate PDF")

    # Save the PDF in the 'pdfs' folder
    pdf_path = "pdfs/invoice_pdf.pdf"
    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(response.content)

    # Update the pdf_file attribute for the invoice object
    invoice.pdf_file = pdf_path
    invoice.save()
    
    return HttpResponse("PDF saved successfully at {}".format(pdf_path))

#finialise order
@login_required
def confirm_order(request, pk):

    #adjust inventory table
    logged_user = request.user
    cart_items = cart.objects.filter(customer=logged_user)
    

    for item in cart_items:
        product_name = item.item
        specific_catalog = item.catalog
        inventory = Inventory.objects.get(name=product_name, catalog_id=specific_catalog)
        ordered_quantity = item.quantity
        quantity_in_stock = inventory.quantity_in_stock
        inventory.quantity_in_stock = max(0, quantity_in_stock - ordered_quantity)
        quantity_sold = inventory.quantity_sold
        inventory.quantity_sold = max(0, quantity_sold + ordered_quantity)
        inventory.sales = float(inventory.cost_per_item) * float(inventory.quantity_sold)
        inventory.save()

    ##add order to order list :-
    #order_id
    invoice = get_object_or_404(Invoice, pk=pk)
    order = invoice.order
   
    #customer name
    customer_name =invoice.billing_name

    # list of products ordered
    cart_products = cart.objects.filter(customer=logged_user)
    grouped_cart_items = cart_products.values('item').annotate(item_count=Sum('quantity'))
    item_list = [f"{group['item_count']}-{group['item']}" for group in grouped_cart_items]
    all_items = ', '.join(item_list)
    
    #total quatities ordered
    total_quantity = cart_products.aggregate(total_quantity=Sum('quantity'))['total_quantity']

    #total amount spent
    amount = invoice.total_amount

    #save order history
    chosen_catalog = Catalog.objects.get(id=cart_items.last().catalog)
    chosen_supplier = User.objects.get(id=chosen_catalog.supplier_id)

    order_entry = Order(
        order_id=order, 
        customer=customer_name,
        product=all_items,
        quantity_ordered=total_quantity,
        amount_spent=amount,
        payment_method = invoice.payment_method,
        payment_status = invoice.payment_status,
        catalog= chosen_catalog.id,
        supplier = chosen_supplier.first_name,
        supplier_email = chosen_supplier.email
        )
    order_entry.save()
    
    customer_order_entry = customerOrderHistory(
        order_id=order, 
        product=all_items,
        quantity_ordered=total_quantity,
        amount_spent=amount,
        customer=request.user.username,
        payment_method = invoice.payment_method,
        payment_status = invoice.payment_status,
        catalog= chosen_catalog.id
    )
    customer_order_entry.save()

    return redirect("confirmation_email", pk=pk)

#send confirmation email with invoice attached to the customer
@login_required
def confirmation_email(request, pk):

    #Generate invoice pdf
    invoice_pdf(request, pk)

    logged_user = request.user
    instruction = "Return to Products"

    #Fetch the invoice from database
    invoice = get_object_or_404(Invoice, pk=pk)
    generated_pdf = "pdfs/invoice_pdf.pdf"

    #Automated mail update
    name = invoice.billing_name
    email_address = invoice.billing_email
    status = ' is currently being processed'
    sender_email = settings.EMAIL_HOST_USER
    email_body = f"""
    Hello, {name}!

    Thank you for placing your order with FarmFresh.

    Please note that your order {status}.
    Attached is the invoice concerning your order. 

    Best regards,
    FarmFresh
    """
    # Create an EmailMessage object
    email = EmailMessage(
    'Order placement successful',
    email_body,
    sender_email,
    [email_address],
    )

    # Attach the PDF to the email
    email.attach_file(generated_pdf)

    # Send the email
    email.send()

    #   clear cart
    cart_table = cart.objects.filter(customer=logged_user)
    cart_table.delete()

    order_amount = OrderAmount.objects.filter(customer=logged_user)
    order_amount.delete()
    request.session['cart_count'] = 0

    note = ""
    if invoice.payment_status == "Pending":
        note = '''  Ensure to settle the payment by the due date specified in the invoice. 
                    Please note that your order can only be shipped and delivered once the payment is complete.
                    Should you not settle the payment by the due date, the order will be canceled.
                    Make sure to upload proof of payment.
                    Payments can be done through EFT or cash deposits at any Discovery Bank ATM. 
                    Use your unique invoice id as reference. 
                    FarmFresh banking details are specified in the invoice.'''
        
    elif invoice.payment_status == "Paid":
        note = '''  Payment successful!
                    Your order will be delivered in approximately 3-5 working days.
                    You will be notified when the order has been shipped and delivered.'''

    context = {
        'instruction': instruction,
        'note': note    
        }
    
    # Notify supplier for order placed
    order = get_object_or_404(Order, order_id=invoice.invoice_no)
    name = order.supplier
    customer = invoice.billing_name
    subject = f"New order placement - id#{invoice.order}!"
    email_address = order.supplier_email
    sender_email = settings.EMAIL_HOST_USER
    email_body = f"""
                Hello, {name}

                Please note that a new order has been placed by {customer}.
                You will be notified when they upload their proof of payment.
                Carefully review the proof of payment prior to approving the order. 

                Best regards,
                FarmFresh
                """
    # Create an EmailMessage object
    email = EmailMessage(
        subject,
        email_body,
        sender_email,
        [email_address],
        )

    # Send the email
    email.send()

    messages.success(request, "Checkout successful")
    return render(request, 'orders/confirm_order.html', context)

# for cleaning trial runs of database
@login_required
def invoice_history(request):
    invoice_history = Invoice.objects.all()
    invoice_history.delete()
    return redirect("order_list")
  
def upload_proof_payment(request, pk):
    customer_order = get_object_or_404(customerOrderHistory, pk=pk)
    invoice = get_object_or_404(Invoice, order=customer_order.order_id)
    if request.method == "POST":
        form = uploadPaymentForm(request.POST, request.FILES, instance=invoice)
        if form.is_valid():
            
            #Update statuses
            customer_order.payment_status = "Paid"
            customer_order.save()

            order = get_object_or_404(Order, order_id=customer_order.order_id)
            order.payment_status = "Paid"
            order.save()

            invoice.payment_status = "Paid"
            invoice.save()
            invoice.payment_proof = form['payment_proof']
            print(f"from invoice: {invoice.order}, from order: {order.order_id}, from customer order: {customer_order.order_id}, invoice number selected:{invoice.id}")
            
            #Notify admin that proof of payment is uploaded by customer
            
            name = order.supplier
            customer = invoice.billing_name
            subject = f"Proof of payment for order id#{invoice.order} uploaded"
            email_address = order.supplier_email
            sender_email = settings.EMAIL_HOST_USER
            email_body = f"""
                Hello, {name}

                Please note that {customer} uploaded their proof of payment for their order.
                Make sure to review the proof of payment prior to approving the order. 

                Best regards,
                FarmFresh
                """
                        # Create an EmailMessage object
            email = EmailMessage(
                        subject,
                        email_body,
                        sender_email,
                        [email_address],
                        )

                        # Send the email
            email.send()
            messages.success(request, "Upload successful")
            return redirect('order_history')
    else:
        form = uploadPaymentForm(instance=invoice)
    return render(request, 'orders/upload_payment.html', {'form': form})

def review_payment(request, id):
    invoice = get_object_or_404(Invoice, order=id)
    if invoice.payment_proof:
        proof = invoice.payment_proof.path
        with open(proof, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="proof of payment.pdf"'
            return response
    else:
        return HttpResponse('The PDF file does not exist.', status=404)