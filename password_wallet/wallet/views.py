from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DeleteView,
    CreateView,
    UpdateView,
    ListView,
    FormView,
    DetailView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Password
from django.urls import reverse_lazy
from .forms import PasswordCreationAndUpdateForm, PasswordCheckForm
from django.shortcuts import get_object_or_404
from .aes import AESCipher
from django.contrib import messages


class PasswordListView(LoginRequiredMixin, ListView):
    model = Password

    def get_queryset(self):
        return Password.objects.filter(user=self.request.user)


class PasswordDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Password
    success_url = reverse_lazy("wallet:wallet")
    success_message = "You successful deleted password!"

    def test_func(self):
        password = self.get_object()
        if self.request.user == password.user:
            return True
        return False


class PasswordCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = PasswordCreationAndUpdateForm
    model = Password
    success_url = reverse_lazy("wallet:wallet")
    success_message = "You successful created password!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if request.user.is_password_checked:
            request.user.is_password_checked = False
            request.user.save()

        return super(PasswordCreateView, self).post(request, *args, **kwargs)


class PasswordUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = PasswordCreationAndUpdateForm
    model = Password
    success_url = reverse_lazy("wallet:wallet")
    success_message = "You successful updated password!"

    def post(self, request, *args, **kwargs):
        if request.user.is_password_checked:
            request.user.is_password_checked = False
            request.user.save()

        return super(PasswordUpdateView, self).post(request, *args, **kwargs)


class IfCheckedView(LoginRequiredMixin, FormView):
    form_class = PasswordCheckForm

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        password = get_object_or_404(Password, pk=pk)

        if password.user != request.user or request.user.is_password_checked:
            return redirect("wallet:show", pk=pk)

        return super(IfCheckedView, self).get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        entered_password = request.POST.get("password")

        if request.user.check_password(entered_password):
            request.user.is_password_checked = True
            request.user.save()

            return redirect("wallet:show", pk=kwargs.get("pk"))

        else:
            messages.error(request, "Password is incorrect!")

        return render(request, "wallet/master_password_check.html", {"form": self.form_class})


class DecryptingPasswordView(DetailView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        password = get_object_or_404(Password, pk=pk)

        if password.user == request.user or not request.user.is_password_checked:
            password = get_object_or_404(Password,
                                         id=pk)
            enc_pass = password.password_to_wallet

            cipher = AESCipher()

            decry_pass = cipher.decrypt(enc_pass.encode())

            return render(request, "wallet/password_show.html", {"password": decry_pass})

        return redirect("wallet:wallet")
