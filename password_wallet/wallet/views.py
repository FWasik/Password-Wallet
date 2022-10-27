from django.shortcuts import render
from django.views.generic import (
    ListView,
    DeleteView,
    CreateView,
    UpdateView,
    ListView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Password
from django.urls import reverse_lazy
from .forms import PasswordCreationAndUpdateForm
from django.shortcuts import get_object_or_404
from .aes import AESCipher


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


class PasswordUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = PasswordCreationAndUpdateForm
    model = Password
    success_url = reverse_lazy("wallet:wallet")
    success_message = "You successful updated password!"


def decrypting_password(request, pk):
    password = get_object_or_404(Password,
                                 id=pk)
    enc_pass = password.password_to_wallet

    cipher = AESCipher()

    decry_pass = cipher.decrypt(enc_pass.encode())

    return render(request, "wallet/password_show.html", {"password": decry_pass})
