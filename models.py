# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountsAccountantpermissions(models.Model):

    class Meta:
        managed = False
        db_table = 'accounts_accountantpermissions'


class AccountsCustomerpermissions(models.Model):

    class Meta:
        managed = False
        db_table = 'accounts_customerpermissions'


class AccountsInventory(models.Model):
    name = models.CharField(max_length=100)
    cost_per_item = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    quantity_in_stock = models.IntegerField()
    quantity_sold = models.IntegerField()
    sales = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    stock_date = models.DateField()
    last_sales_date = models.DateField()
    is_deleted = models.BooleanField()
    barcode = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    sales_data = models.JSONField(blank=True, null=True)
    farmer = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts_inventory'


class AccountsRating(models.Model):
    rating = models.IntegerField()
    inventory = models.ForeignKey(AccountsInventory, models.DO_NOTHING)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_rating'


class AccountsSalesdata(models.Model):
    date = models.DateField()
    quantity_sold = models.IntegerField()
    product = models.ForeignKey(AccountsInventory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_salesdata'


class AccountsStaffpermissions(models.Model):

    class Meta:
        managed = False
        db_table = 'accounts_staffpermissions'


class AccountsSubscriber(models.Model):
    email = models.CharField(unique=True, max_length=254)
    subscribed_at = models.DateTimeField()
    is_active = models.BooleanField()
    receive_marketing_emails = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'accounts_subscriber'


class AccountsSupplierpermissions(models.Model):

    class Meta:
        managed = False
        db_table = 'accounts_supplierpermissions'


class AccountsTestimonial(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField()
    inventory = models.ForeignKey(AccountsInventory, models.DO_NOTHING)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_testimonial'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class OrdersCart(models.Model):
    item = models.CharField(max_length=100)
    cost_per_item = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    customer = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'orders_cart'


class OrdersCartRecords(models.Model):
    item = models.CharField(max_length=100)
    cost_per_item = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    customer = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'orders_cart_records'


class OrdersCustomerorderhistory(models.Model):
    order_id = models.CharField(max_length=100)
    order_date = models.DateTimeField()
    customer = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    quantity_ordered = models.PositiveIntegerField(blank=True, null=True)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    customer_order_status = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'orders_customerorderhistory'


class OrdersInvoice(models.Model):
    date_created = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    billing_name = models.CharField(max_length=255)
    billing_address = models.TextField()
    billing_email = models.CharField(max_length=254)
    payment_status = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20)
    payment_due_date = models.DateField(blank=True, null=True)
    notes = models.TextField()
    status = models.CharField(max_length=20)
    pdf_file = models.CharField(max_length=100, blank=True, null=True)
    payment_proof = models.CharField(max_length=100, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    invoice_no = models.CharField(max_length=255)
    order = models.CharField(max_length=255)
    supplier_info = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders_invoice'


class OrdersOrder(models.Model):
    order_id = models.CharField(max_length=100)
    order_date = models.DateTimeField()
    customer = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    quantity_ordered = models.PositiveIntegerField(blank=True, null=True)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    payment_method = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    order_status = models.CharField(max_length=20)
    catalog = models.ForeignKey('AccountsCatalog', models.DO_NOTHING, blank=True, null=True)
    supplier_email = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders_order'


class OrdersOrderamount(models.Model):
    amount_due = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    customer = models.CharField(max_length=100)
    cart_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders_orderamount'


class SocialAuthAssociation(models.Model):
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'social_auth_association'
        unique_together = (('server_url', 'handle'),)


class SocialAuthCode(models.Model):
    email = models.CharField(max_length=254)
    code = models.CharField(max_length=32)
    verified = models.BooleanField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_code'
        unique_together = (('email', 'code'),)


class SocialAuthNonce(models.Model):
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=65)

    class Meta:
        managed = False
        db_table = 'social_auth_nonce'
        unique_together = (('server_url', 'timestamp', 'salt'),)


class SocialAuthPartial(models.Model):
    token = models.CharField(max_length=32)
    next_step = models.PositiveSmallIntegerField()
    backend = models.CharField(max_length=32)
    timestamp = models.DateTimeField()
    data = models.JSONField()

    class Meta:
        managed = False
        db_table = 'social_auth_partial'


class SocialAuthUsersocialauth(models.Model):
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    extra_data = models.JSONField()

    class Meta:
        managed = False
        db_table = 'social_auth_usersocialauth'
        unique_together = (('provider', 'uid'),)


class TransactionsPurchasebill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField()
    supplier = models.ForeignKey('TransactionsSupplier', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'transactions_purchasebill'


class TransactionsPurchasebilldetails(models.Model):
    eway = models.CharField(max_length=50, blank=True, null=True)
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)
    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.CharField(max_length=50, blank=True, null=True)
    billno = models.ForeignKey(TransactionsPurchasebill, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'transactions_purchasebilldetails'


class TransactionsPurchaseitem(models.Model):
    quantity = models.IntegerField()
    perprice = models.IntegerField()
    totalprice = models.IntegerField()
    billno = models.ForeignKey(TransactionsPurchasebill, models.DO_NOTHING)
    stock = models.ForeignKey(AccountsInventory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'transactions_purchaseitem'


class TransactionsSupplier(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(unique=True, max_length=12)
    address = models.CharField(max_length=200)
    email = models.CharField(unique=True, max_length=254)
    is_deleted = models.BooleanField()
    reg_no = models.CharField(unique=True, max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transactions_supplier'


class UserProfile(models.Model):
    avatar = models.CharField(max_length=100)
    bio = models.TextField()
    phone_number = models.CharField(max_length=128, blank=True, null=True)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)
    address = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_profile'
