from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DeleteView,
    CreateView,
    UpdateView,
    ListView,
    FormView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Password
from django.urls import reverse_lazy
from .forms import PasswordCreationAndUpdateForm, PasswordCheckForm
from django.shortcuts import get_object_or_404
from .aes import AESCipher
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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


class IfCheckedView(FormView):
    form_class = PasswordCheckForm

    def get(self, request, *args, **kwargs):
        if request.user.is_password_checked:
            return redirect("wallet:show", pk=kwargs["pk"])

        return super(IfCheckedView, self).get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        entered_password = request.POST["password"]

        if request.user.check_password(entered_password):
            request.user.is_password_checked = True
            request.user.save()

            return redirect("wallet:show", pk=kwargs["pk"])

        else:
            messages.error(request, "Password is incorrect!")

        return render(request, "wallet/master_password_check.html", {"form": self.form_class})


@login_required
def decrypting_password(request, pk):
    password = get_object_or_404(Password,
                                 id=pk)
    enc_pass = password.password_to_wallet

    cipher = AESCipher()

    decry_pass = cipher.decrypt(enc_pass.encode())

    return render(request, "wallet/password_show.html", {"password": decry_pass})
