from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myass.models import Room
from .serializers import RoomSerializer

@api_view(['GET','PUT','POST'])
def getRoutes(request):
    routes=[
        'GET/api',
        'GET/api/rooms',
        'GET/api/rooms/:id'
    ]
    
    return  Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms=Room.objects.all()#Objects cannot be converted directly to a Json response
    serializer=RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request,pk):
    room=Room.objects.get(id=pk)#Objects cannot be converted directly to a Json response
    serializer=RoomSerializer(room, many=False)
    return Response(serializer.data)