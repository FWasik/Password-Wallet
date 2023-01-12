from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.urls import reverse_lazy
from BruteBuster.models import FailedAttempt
from django.contrib import messages

from .models import Address


@login_required
def get_logs_view(request):
    if request.method == "GET":
        query_is_successful = Address.objects.filter(username=request.user.login)\
                                             .select_related('log')\
                                             .values("IP", "log__failures", "log__pk")\
                                             .annotate(num_of_succ=Count("is_successful", filter=Q(is_successful=True)),
                                                       num_of_unsucc=Count("is_successful", filter=Q(is_successful=False)))\


        query_details = Address.objects.filter(username=request.user.login)\
                                       .values("pk", "IP", "time", "is_successful")\
                                       .order_by("-time")

        data = {
            "query_is_successful": query_is_successful,
            "query_details": query_details
        }

        return render(request, "addresses/addresses.html", {"data": data})


@login_required
def unblock_address_view(request, pk):
    log = FailedAttempt.objects.get(pk=pk)

    log.failures = 0
    log.save()

    messages.success(request, f"You successful unblocked address: {log.IP}")

    return redirect(reverse_lazy('addresses:list'))


@login_required
def delete_address_view(request, pk):
    log = FailedAttempt.objects.get(pk=pk)
    ip_addr = log.IP
    log.delete()

    messages.success(request, f"You successful delete address: {ip_addr}")

    return redirect(reverse_lazy('addresses:list'))


@login_required
def delete_address_log_view(request, pk):
    Address.objects.get(username=request.user.login, pk=pk).delete()

    messages.success(request, f"You successful delete log!")

    return redirect(reverse_lazy('addresses:list'))


@login_required
def delete_all_address_logs_view(request):
    Address.objects.filter(username=request.user.login).delete()

    messages.success(request, f"You successful delete all logs!")

    return redirect(reverse_lazy('addresses:list'))
