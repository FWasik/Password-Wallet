from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash, authenticate, login as auth_login
from django.views.generic import DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.urls import views as auth_views
from datetime import datetime
from ipware import get_client_ip
from BruteBuster.models import FailedAttempt

from .models import CustomUser
from .forms import CustomUserCreationForm
from addresses.models import Address


class CustomUserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")
    success_message = "You successful registered user!"


class CustomUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("users:login")
    success_message = "You successful deleted account!"

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False


class CustomUserDetailView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = get_user_model()

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False


class CustomLogoutView(auth_views.LogoutView):
    def get(self, request, *args, **kwargs):
        request.user.is_password_checked = False
        request.user.save()

        messages.success(request, "You have been log out!")

        return super(CustomLogoutView, self).get(request, *args, **kwargs)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.is_password_checked = False
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:password-change')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {
        'form': form
    })


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        current_ip = get_client_ip(request)[0]
        was_blocked = False
        failures = 0

        # request.META["REMOTE_ADDR"] = "0.0.0.0"
        # current_ip = request.META["REMOTE_ADDR"]

        try:
            log = FailedAttempt.objects.get(username=username, IP=current_ip)
        except FailedAttempt.DoesNotExist:
            log = None

        if log and log.failures > 4 and log.IP == current_ip:
            log.failures += 1
            log.save()

            messages.error(request,
                           'You have typed incorrect credentials at least 5 times in a row. Login is blocked '
                           ' at this IP address permanently. Contact administrator',
                           extra_tags='block alert-danger')

            Address.objects.create(IP=current_ip, username=username, is_successful=False, log=log)

            return redirect(reverse_lazy('users:login'))

        elif log and 1 < log.failures < 5:
            failures = log.failures
            was_blocked = True

        user = authenticate(request=request, username=username, password=password)
        try:
            log = FailedAttempt.objects.get(username=username, IP=current_ip)
        except FailedAttempt.DoesNotExist:
            log = FailedAttempt.objects.create(username=username, IP=current_ip)

        if user:
            if user.is_active:
                auth_login(request, user)
                Address.objects.create(IP=current_ip, username=username, is_successful=True, log=log)
                return redirect(reverse_lazy('wallet:wallet'))
        else:
            try:
                user = CustomUser.objects.get(login=username)

            except CustomUser.DoesNotExist:
                user = None

            if user:
                user.unsuccessful_time_login = datetime.now()
                user.save()

            if log.blocked():
                display_message(request, log)

            elif was_blocked:
                log.failures = failures + 1
                log.save()

                display_message(request, log)

            else:
                messages.error(request, 'Username or password not correct', extra_tags='block alert-danger')

            Address.objects.create(IP=current_ip, username=username, is_successful=False, log=log)

            return redirect(reverse_lazy('users:login'))

    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def display_message(request, log: FailedAttempt) -> None:
    if log.failures > 4:
        messages.error(request,
                       'You have typed incorrect credentials at least 5 times in a row. Login is blocked '
                       ' at this IP address permanently. Contact administrator',
                       extra_tags='block alert-danger')

    else:
        messages.error(request, f'You have typed incorrect credentials {log.failures} times in a row. Login is '
                                'blocked for 2 minutes. Last login attempted: '
                                f'{log.timestamp.strftime("%Y-%m-%d %H:%M:%S")}',
                       extra_tags='block alert-danger')
