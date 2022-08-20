from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room, Poll
from .serializers import RoomSerializer, OptionSerializer
from base.api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/polls/:id',
    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getOptions(request, pk):
    room = Room.objects.get(id=pk)
    poll = Poll.objects.get(room=room)
    options = poll.option_set.all()
    serializer = OptionSerializer(options, many=True)
    return Response(serializer.data)
