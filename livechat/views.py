from django.shortcuts import render, redirect
from django.utils.text import slugify
from .models import Room


def index(request):
    # eski noto'g'ri room nomlarini slug formatga o'tkazish
    for room in Room.objects.all():
        fixed_name = slugify(room.name)
        if fixed_name and fixed_name != room.name:
            room.name = fixed_name
            room.save()

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        room_name = request.POST.get("room_name", "").strip()

        room_slug = slugify(room_name)

        if username and room_slug:
            request.session["chat_username"] = username
            Room.objects.get_or_create(name=room_slug)
            return redirect("room", room_name=room_slug)

    rooms = Room.objects.all().order_by("name")
    return render(request, "livechat/index.html", {"rooms": rooms})


def room(request, room_name):
    username = request.session.get("chat_username", "")
    room, _ = Room.objects.get_or_create(name=room_name)
    messages = room.messages.all()[:100]
    rooms = Room.objects.all().order_by("name")

    return render(
        request,
        "livechat/room.html",
        {
            "room_name": room_name,
            "username": username,
            "messages": messages,
            "rooms": rooms,
        },
    )