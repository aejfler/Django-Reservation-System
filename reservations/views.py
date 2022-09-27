import datetime
from django.db.models import OuterRef, Exists
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, get_list_or_404
from .forms import AddRoomForm, ModifyRoomForm, ReservationForm
from reservations.models import Room, Reservation


def start(request):
    return render(request, 'home.html')


def add_room(request):
    if request.method == "GET":
        return render(request, "add_room.html")
    elif request.method == "POST":
        form = AddRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("rooms")
        else:
            return HttpResponse("Room already exists!")


def list_of_rooms(request):
    rooms = Room.objects.order_by("name")
    if request.GET.get('filter', 'clear') == 'apply':
        filters = request.GET
        filter_name = filters.get('filter_name', '')
        filter_capacity_from = int(filters.get('filter_capacity_from', 0) or 0)
        filter_capacity_to = int(filters.get('filter_capacity_to', 0) or 0)
        filter_projector_availability = bool(filters.get('filter_projector_availability', False) or False)
        filter_date = filters.get('filter_date', '')
        if filter_date:
            filter_date = datetime.datetime.strptime(filter_date, '%Y-%m-%d')
        if filter_name:
            rooms = rooms.filter(name__contains=filter_name)
        if filter_capacity_from:
            rooms = rooms.filter(capacity__gt=filter_capacity_from)
        if filter_capacity_to:
            rooms = rooms.filter(capacity__lte=filter_capacity_to)
        if filter_projector_availability:
            rooms = rooms.filter(projector_availability=True)
        if filter_date:
            rooms = rooms.filter(~Exists(Reservation.objects.filter(date=filter_date, room_id=OuterRef('pk'))))
    # if clear filters was clicked check -> else
    else:
        filters = {
            "filter_name": '',
            "filter_capacity_from": '',
            "filter_capacity_to": '',
            "filter_projector_availability": False,
        }
    context = {
        "rooms": rooms,
        "filter": filters,
    }
    return render(request, "rooms_list.html", context)


def delete_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == "GET":
        room.delete()
        return HttpResponse("Room was deleted!")
    return redirect('rooms')


def modify_room(request, room_id):
    room_id = get_object_or_404(Room, pk=room_id)
    if request.method == "GET":
        form = ModifyRoomForm(instance=room_id)
        return render(request, "modify_room.html", {"form": form})
    elif request.method == "POST":
        form = ModifyRoomForm(request.POST, instance=room_id)
        if form.is_valid():
            form.save()
            return redirect('rooms')
        return render(request, "modify_room.html", {"form": form})


def reservation(request, pk):
    rooms = get_object_or_404(Room, pk=pk)
    if request.method == "GET":
        form = ReservationForm()

    elif request.method == "POST":
        form = ReservationForm(request.POST)
        ''' completing some form data from other sources '''
        form.instance.room = rooms  # room was not sent in POST data
        if form.is_valid():
            form.save()
            return redirect('rooms')
    return render(request, "reservation.html",  {"form": form, "rooms": rooms})


def all_reservations(request):
    reserv = get_list_or_404(Reservation)
    if request.method == "GET":
        return render(request, "reserved_list.html", context={"reserv": reserv})


def cancel_reservation(request, pk):
    reservations = get_object_or_404(Reservation, pk=pk)
    if request.method == "POST":
        reservations.delete()
        return redirect('rooms')
    else:
        context = {
            "reservations": reservations,
        }
    return render(request, "cancel_reservation.html", context)


def detail_view(request, room_id):
    if request.method == "GET":
        room = Room.objects.get(id=room_id)
        reservation_dates = [reservation.date for reservation in room.reservations_dated()]
        return render(request, "room_details.html", {"room": room, 'reservation_dates': reservation_dates})


def availability(request):

    rooms = Room.objects.all().order_by('name')
    for room in rooms:
        ''' those dates are available for all rooms'''
        reservation_dates = [reservation.date for reservation in room.reservations.all()]

        '''here choosing dates that already booked '''
        room.reserved = datetime.date.today() in reservation_dates
        return render(request, "availability.html", {"rooms": rooms})
