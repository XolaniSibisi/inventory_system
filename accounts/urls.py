from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('catalog/', login_required(views.catalog_list), name='catalog_list'),
    path('catalog_create/', views.catalog_create, name='catalog_create'),
    path('upload_catalog/', views.upload_catalog, name='upload_catalog'),
    path('extract_catalog_data/<int:pk>/', views.extract_catalog_data, name='extract_catalog_data'),
    path('products/', login_required(views.products), name='products'),
    path('per_product/<int:pk>/', login_required(views.per_product), name='per_product'),
    path('each_product/<int:pk>/', login_required(views.each_product), name='each_product'),
    path("product_update/<int:pk>/", login_required(views.update), name="product_update"),
    path("delete/<int:pk>/", login_required(views.delete), name="product_delete"),
    path("add/", login_required(views.add_product), name="product_add"),
    path('marketing/', login_required(views.marketing), name='marketing'),
    path("dashboard/", login_required(views.dashboard), name="dashboard"),
    path('about/', login_required(views.about), name='about'),
    path('search/', login_required(views.search), name='search'),
    path('generate_sales_report/', login_required(views.generate_sales_report), name='generate_sales_report'),
    path('analyze-sales-data/', views.analyze_sales_data, name='analyze_sales_data'),
    path('subscription/', login_required(views.subscription), name='subscription'),
    path('send_bulk_emails/',login_required(views.send_bulk_emails), name='send_bulk_emails'),
    path('create_inventory/', login_required(views.create_inventory), name='create_inventory'),
    path('inventory_list/', login_required(views.inventory_list), name='inventory_list'),
    path('rate/', login_required(views.rate), name='rate'),
    path('rate_inventory/<int:inventory_id>/', login_required(views.rate_inventory), name='rate_inventory'),
    path('distributor/', login_required(views.distributor), name='distributor'),
    path('distributor_list/', login_required(views.distributor_list), name='distributor_list'),
    path('write_review/<int:pk>/', login_required(views.write_review), name='write_review'),
    path('delete_testimonial/<int:testimonial_id>/', login_required(views.delete_testimonial), name='delete_testimonial'),
    path('update_testimonial/<int:testimonial_id>/', login_required(views.update_testimonial), name='update_testimonial'),
    path('nearby_suppliers/', login_required(views.nearby_suppliers), name='nearby_suppliers'),
    path('each_catalog/<int:catalog_id>/', views.each_catalog, name='each_catalog'),
]