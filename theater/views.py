from rest_framework import viewsets

from theater.models import Actor, Genre
from theater.serializers import ActorSerializer, GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
