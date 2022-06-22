from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Note
from api.serializers import NoteSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting note'
        },
    ]

    return Response(routes)


@api_view(['GET'])
def getNotes(request):
    notes = Note.objects.all().order_by('-updated')
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getNote(request, pk):
    try:
        note = Note.objects.get(id=pk)
    except Note.DoesNotExist:
        return Response({'message': f'id {pk} not found!'}, status.HTTP_404_NOT_FOUND)
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)


@api_view(['PATCH'])
def updateNote(request, pk):
    data = request.data
    try:
        note = Note.objects.get(id=pk)
    except Note.DoesNotExist:
        return Response({'message': f'id {pk} not found!'}, status.HTTP_404_NOT_FOUND)
    serializer = NoteSerializer(instance=note, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteNote(request, pk):
    try:
        note = Note.objects.get(id=pk)
    except Note.DoesNotExist:
        return Response({'message': f'id {pk} not found!'}, status.HTTP_404_NOT_FOUND)
    note.delete()
    return Response({'message': f'note {pk} was deleted!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def createNote(request):
    data = request.data
    serializer = NoteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
