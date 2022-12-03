from django.shortcuts import render
from django.views import View
from room_reservation import models
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import datetime


class AddRoom(View):
    def get(self, request):
        return render(request, "Add.html")

    def post(self, request):
        name = request.POST.get("room_name")
        seats = int(request.POST.get("seats"))
        projector = request.POST.get("projector")
        if projector == "yes":
            projector = True
        elif projector == "no":
            projector = False
        if name == "":
            ctx = {"error_name": "Room name cannot be empty"}
            return render(request, "Add.html", ctx)
        if seats < 1 or not isinstance(seats, int):
            ctx = {"error_name": "Number of seats has to be an integer bigger than 0"}
            return render(request, "Add.html", ctx)
        try:
            models.Room.objects.get(name=name)
            ctx = {"error_name": f"A room with the same name already exists"}
            return render(request, "Add.html", ctx)
        except ObjectDoesNotExist:
            models.Room.objects.create(name=name, seats=seats, projector=projector).save()
            ctx = {"error_name": f"The room {name} has been successfully added!"}
            return render(request, "Add.html", ctx)

def home(request):
    room_list = models.Room.objects.all()
    reservation_list = models.RoomReservation.objects.all()
    today = datetime.date.today()
    for room in room_list:
        res_dates = [reservation.date for reservation in room.roomreservation_set.all()]
        room.reserved = datetime.date.today() in res_dates
    ctx = {'room_list': room_list}
    return render(request, "Home.html", ctx)

class DeleteRoom(View):
    def get(self, request, room_id):
        room = models.Room.objects.get(id=room_id)
        ctx = {'room': room}
        return render(request, "Delete_get.html", ctx)
    def post(self, request, room_id):
        room = models.Room.objects.get(id=room_id)
        ctx = {'room': room}
        room.delete()
        return render(request, "Delete_post.html", ctx)

class EditRoom(View):
    def get(self, request, room_id):
        room = models.Room.objects.get(id=room_id)
        ctx = {'room': room}
        return render(request, "Edit_get.html", ctx)
    def post(self, request, room_id):
        room = models.Room.objects.get(id=room_id)
        name = request.POST.get("room_name")
        seats = int(request.POST.get("seats"))
        projector = request.POST.get("projector")
        if projector == "yes":
            projector = True
        elif projector == "no":
            projector = False
        if name == "":
            ctx = {"error_name": "Room name cannot be empty"}
            return render(request, "Edit_get.html", ctx)
        if seats < 1 or not isinstance(seats, int):
            ctx = {"error_name": "Number of seats has to be an integer bigger than 0"}
            return render(request, "Edit_get.html", ctx)
        try:
            models.Room.objects.get(name=name)
            ctx = {"error_name": f"A room with the same name already exists"}
            return render(request, "Edit_get.html", ctx)
        except ObjectDoesNotExist:
            room.name = name
            room.seats = seats
            room.projector = projector
            room.save()
            ctx = {"error_name": f"The room {name} has been successfully edited!"}
            return render(request, "Edit_get.html", ctx)

class ReserveRoom(View):

    def get(self, request, room_id):
        room = models.Room.objects.get(id=room_id)
        reservations = models.RoomReservation.objects.filter(id=room_id).order_by('date')
        ctx = {'room': room, 'reservations': reservations}
        return render(request, "Reserve_get.html", ctx)

    def post(self, request, room_id):
        room = models.Room.objects.get(id=room_id)
        comment = request.POST.get('comment')
        res_date = request.POST.get('date')
        if res_date < str(datetime.date.today()):
            ctx = {'room': room, 'result': f'Error: the date {res_date} is in the past'}
            return render(request, "Reserve_get.html", ctx)
        try:
            models.RoomReservation.objects.create(room_id=room, comment=comment, date=res_date)
            ctx = {'room': room, 'result': f'Room {room.name} has been successfully booked for {res_date}'}
            return render(request, "Reserve_get.html", ctx)
        except:
            ctx = {'room': room, 'result': f'Room {room.name} could not be booked for {res_date}'}
            return render(request, "Reserve_get.html", ctx)

class RoomInfo(View):
    def get(self, request, room_id):
        room = models.Room.objects.get(id=room_id)
        reservations = models.RoomReservation.objects.filter(id=room_id).order_by('date')
        ctx = {'room': room, 'reservations': reservations}
        return render(request, "Room_info.html", ctx)
