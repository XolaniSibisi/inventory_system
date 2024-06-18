from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Profile
from user.forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from orders.models import Invoice, cart, cart_records, customerOrderHistory, OrderAmount


@login_required
def logout(request):
    return redirect(to='')

# custom 404 view


@login_required
def custom_404(request, exception):
    return render(request, 'users/404.html', status=404)


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        is_supplier = request.user.groups.filter(name='supplier').exists()
        is_distributor = request.user.groups.filter(name='distributor').exists()
        
        return render(request, self.template_name, {'form': form, 'is_supplier': is_supplier, 'is_distributor': is_distributor})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            print("Form data:", request.POST)
            # Save the form data but don't commit to the database yet
            user = form.save(commit=False)

            role = form.cleaned_data['role']

            group_name = ''

            if role == 'customer':
                group_name = 'customer'
            elif role == 'admin':
                group_name = 'admin'
            elif role == 'supplier':
                group_name = 'supplier'
            elif role == 'distributor':
                group_name = 'distributor'

            try:
                group = Group.objects.get(name=group_name)
            except ObjectDoesNotExist:
                # Create the group if it doesn't exist
                group = Group.objects.create(name=group_name)

            if role == 'admin':
                user.is_superuser = True
                user.is_staff = True

            user.save()  # Now commit the changes to the database

            user.groups.add(group)  # Add the user to the group after saving

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})

# Class based view that extends from the built in login view to add a remember me functionality


class CustomLoginView(LoginView, SuccessMessageMixin):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('login')


@login_required
def profile(request):
    logged_user = request.user
    profile_info = Profile.objects.get(user_id=logged_user.id)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

        # update order management
    customer_name = request.session.get('old_username', None)
    if customer_name is not None:
        Invoice.objects.filter(billing_name=customer_name).update(billing_email=logged_user.email)
        cart.objects.filter(customer=customer_name).update(customer=request.user.username)
        customerOrderHistory.objects.filter(customer=customer_name).update(customer=request.user.username)
        cart_records.objects.filter(customer=customer_name).update(customer=request.user.username)
        OrderAmount.objects.filter(customer=customer_name).update(customer=request.user.username)
    
    users = None
    if request.user.is_superuser:
        users = User.objects.exclude(is_superuser=True)
        
    if request.user.is_superuser:
        return render(request, 'users/admin_profile.html', {'users': users})
    else:
        return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form, 'profile': profile_info, 'user': logged_user})


@login_required
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # You can fetch additional information related to the user if needed
    return render(request, 'users/view_user.html', {'user': user})
