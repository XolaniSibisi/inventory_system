from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('invoice', login_required(views.invoice_detail), name='invoice_detail'),
    path('edit_invoice/<int:pk>/', login_required(views.edit_invoice), name='edit_invoice'),
    path('delete_invoice/<int:pk>/', login_required(views.delete_invoice), name='delete_invoice'),
    path('order_list', login_required(views.order_list), name='order_list'),
    path('update_order_status/<int:order_id>/', login_required(views.update_order_status), name='update_order_status'),
    path('order_history', login_required(views.order_history), name='order_history'),
    path('return_order/<int:order_id>/', login_required(views.return_order), name='return_order'),
    path('invoice_pdf/<int:pk>/', login_required(views.invoice_pdf), name='invoice_pdf'),
    path('view_cart', login_required(views.view_cart), name='view_cart'),
    path('delete_from_cart/<int:item_id>/', login_required(views.delete_from_cart), name="delete_from_cart"),
    path('increase_cart_quantity/<int:item_id>/', login_required(views.increase_cart_quantity), name="increase_cart_quantity"),
    path('decrease_cart_quantity/<int:item_id>/', login_required(views.decrease_cart_quantity), name="decrease_cart_quantity"),
    path('add_to_cart/<int:item_id>/', login_required(views.add_to_cart), name="add_to_cart"),
    path('delete_cart', login_required(views.delete_cart), name='delete_cart'),
    path('order_details', login_required(views.order_details), name='order_details'),
    path('confirm_order/<int:pk>/', login_required(views.confirm_order), name='confirm_order'),
    path('confirmation_email/<int:pk>/', login_required(views.confirmation_email), name='confirmation_email'),
    path('invoice_history', login_required(views.invoice_history), name='invoice_history'),
    path('upload_proof_payment/<int:pk>/', login_required(views.upload_proof_payment), name='upload_proof_payment'),
    path('review_payment/<str:id>/', login_required(views.review_payment), name='review_payment'),
]

