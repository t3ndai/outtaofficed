from django.shortcuts import render
from django.http import HttpResponse

from gripcontrol import HttpStreamFormat
from django_grip import set_hold_stream, publish
from django_eventstream import send_event

# Create your views here.
def item_subscribe(request, item_id):
    client_details = {"id": request.user.pk, "item": item_id}
    set_hold_stream(request, f"items/{item_id}")
    # send_event(f"items/{item_id}", "message", {"text": "connected"})
    return HttpResponse(
        "event: message\ndata: connected\n\n", content_type="text/event-stream"
    )
