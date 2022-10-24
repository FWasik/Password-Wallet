from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            login = form.cleaned_data.get("login")
            messages.success(request, f"You successful registered user named {login}")
            return redirect("users-login")

        else:
            messages.error(request, f"You didn't register user! Check fields again!")

    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {"form": form})
