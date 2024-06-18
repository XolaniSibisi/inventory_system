# accounts/management/commands/update_suppliers.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from user.models import Profile

class Command(BaseCommand):
    help = 'Update supplier status for profiles based on group membership'

    def handle(self, *args, **kwargs):
        # Fetch the "Suppliers" group
        try:
            group = Group.objects.get(name='supplier')
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR('Group "Suppliers" does not exist. Please create the group.'))
            return

        # Fetch users belonging to the "Suppliers" group
        supplier_users = group.user_set.all()

        # Loop through the users and update the is_supplier field for corresponding profiles
        for user in supplier_users:
            try:
                profile = Profile.objects.get(user=user)
                profile.is_supplier = True
                profile.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully updated supplier status for {user.username}'))
            except Profile.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'No profile found for user: {user.username}'))
