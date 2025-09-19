from rest_framework import viewsets

from theater.models import Actor, Genre, Play, TheaterHall, Reservation
from theater.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlayListRetrieveSerializer,
    PlayListCreateSerializer,
    PlayDetailSerializer,
    ActorDetailSerializer,
    TheaterHallSerializer,
    ReservationSerializer,
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


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)
