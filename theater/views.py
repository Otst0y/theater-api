from rest_framework import viewsets

from theater.models import Actor, Genre, Play, TheaterHall
from theater.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlayListRetrieveSerializer,
    PlayListCreateSerializer,
    PlayDetailSerializer,
    ActorDetailSerializer,
    TheaterHallSerializer,
)


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ActorDetailSerializer
        return ActorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class PlayViewSet(viewsets.ModelViewSet):
    serializer_class = PlayListRetrieveSerializer
    queryset = Play.objects.all()
    action_serializer_classes = {
        "create": PlayListCreateSerializer,
        "retrieve": PlayDetailSerializer,
        "update": PlayListCreateSerializer,
        "patrial_update": PlayListCreateSerializer,
    }

    def get_serializer_class(self):
        return self.action_serializer_classes.get(self.action, self.serializer_class)


class TheaterHallViewSet(viewsets.ModelViewSet):
    serializer_class = TheaterHallSerializer
    queryset = TheaterHall.objects.all()
