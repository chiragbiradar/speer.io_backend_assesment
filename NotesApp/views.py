from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Note, CustomUser
from .serializers import NoteSerializer, ProfileSerializer
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity, SearchVector
from django.db.models import Q
from django_ratelimit.decorators import ratelimit


###
#Login User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#Register User
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@api_view(['GET'])
@ratelimit(key='ip', rate='100/h')
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/',
        '/api/prediction/'
        'api/notes/',
        'api/note/<int:pk>/',
        'api/note/<int:pk>/update/',
        'api/note/<int:pk>/delete/',
        'api/note/mynotes/',
        'api/notes/create/',
        'api/profile/',
        'api/profile/update/',
        'api/users/<int:pk>/notes',

    ]
    return Response(routes)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/h')
def getNotes(request):
    if request.method == 'GET':
        user_notes = request.user.notes.all().order_by('-updated')[:10]
        shared_notes = Note.objects.filter(shared_users=request.user)  
        notes = user_notes | shared_notes
        serializer = NoteSerializer(notes, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        user = request.user
        data = request.data
        note = Note.objects.create(
            user=user,
            title=data['title'],
            body=data['body'],
        )
        serializer = NoteSerializer(note, many=False, context={'request': request})
        return Response(serializer.data)

#api/notes/<int:pk>
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/h')
def getNote(request, pk):
    note = request.user.notes.get(id=pk)
    serializer = NoteSerializer(note, many=False, context={'request': request})
    return Response(serializer.data)

#api/notes/<int:pk>/update
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/h')
def updateNote(request, pk):
    note = request.user.notes.get(id=pk)
    serializer = NoteSerializer(instance=note, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#api/notes/<int:pk>/delete
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/h')
def deleteNote(request, pk):
    note = request.user.notes.get(id=pk)
    note.delete()
    return Response('Note was deleted')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/h')
def getProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/h')
def updateProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#api/notes/user/<int:pk>/mynotes
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/h')
def getUserNotes(request, pk):
    user = CustomUser.objects.get(id=pk)
    notes = Note.objects.filter(user=user)
    serializer = NoteSerializer(notes, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/h')
def share(request, pk):
        note = get_object_or_404(Note, pk=pk, user=request.user)
        user_to_share = get_object_or_404(CustomUser, pk=request.data['user_id'])
        if user_to_share == request.user:
            return Response("Cannot share a note with yourself", status=status.HTTP_400_BAD_REQUEST)
        if user_to_share in note.shared_users.all():
            return Response("User already has access to this note", status=status.HTTP_400_BAD_REQUEST)
        note.shared_users.add(user_to_share)
        note.save()
        serializer = NoteSerializer(note, context={'request': request})
        return Response(serializer.data)    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/h')
def searchNote(request):
        query = request.GET.get('q')
        if query:
            vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            notes = Note.objects.annotate(
                rank=SearchRank(vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')  # Adjust rank threshold as needed
            notes = notes.filter(Q(owner=request.user) | Q(shared_users=request.user))  # Restrict to accessible notes
            serializer = NoteSerializer(notes, many=True, context={'request': request})
            return Response(serializer.data)
        return Response({'error': 'Please provide a query parameter.'}, status=400)
