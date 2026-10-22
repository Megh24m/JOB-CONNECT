from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Notification


@login_required
def notifications(request):
    notes = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    # Fetch settings to check date/time display
    show_datetime = True
    if hasattr(request.user, 'seeker_settings'):
        show_datetime = request.user.seeker_settings.show_datetime

    return render(
        request,
        "notifications.html",
        {
            "notifications": notes,
            "show_datetime": show_datetime,
        }
    )


@login_required
def mark_as_read(request, id):
    note = get_object_or_404(Notification, id=id, user=request.user)
    note.is_read = True
    note.save()

    # If it is linked to an application, take them there so they can respond
    if note.application:
        return redirect("my_applications")

    return redirect("notifications")