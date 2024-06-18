
def user_group(request):
    is_customer = request.user.groups.filter(name='customer').exists()
    is_supplier = request.user.groups.filter(name='supplier').exists()
    is_distributor = request.user.groups.filter(name='distributor').exists()
    return {'is_customer': is_customer, 'is_supplier': is_supplier, 'is_distributor': is_distributor}