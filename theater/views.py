from rest_framework import viewsets
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)

from theater.models import (
    Actor,
    Genre,
    Play,
    TheaterHall,
    Reservation,
    Performance,
    Ticket,
)
from theater.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlayListRetrieveSerializer,
    PlayListCreateSerializer,
    PlayDetailSerializer,
    ActorDetailSerializer,
    TheaterHallSerializer,
    ReservationSerializer,
    PerformanceListSerializer,
    PerformanceCreateSerializer,
    PerformanceDetailSerializer,
    TicketCreateSerializer,
    TicketListSerializer,
    TicketDetailSerializer,
)


class ActionBasedPermissionMixin:
    action_permission_classes = {}

    def get_permissions(self):
        permission_classes = self.action_permission_classes.get(
            self.action, [IsAuthenticated]
        )
        return [permission() for permission in permission_classes]


class ActorViewSet(ActionBasedPermissionMixin, viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    action_permission_classes = {
        "create": [IsAdminUser],
        "update": [IsAdminUser],
        "partial_update": [IsAdminUser],
        "destroy": [IsAdminUser],
        "list": [IsAuthenticatedOrReadOnly],
        "retrieve": [IsAuthenticatedOrReadOnly],
    }

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ActorDetailSerializer
        return ActorSerializer


class GenreViewSet(ActionBasedPermissionMixin, viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    action_permission_classes = {
        "create": [IsAdminUser],
        "update": [IsAdminUser],
        "partial_update": [IsAdminUser],
        "destroy": [IsAdminUser],
        "list": [IsAuthenticatedOrReadOnly],
        "retrieve": [IsAuthenticatedOrReadOnly],
    }


class PlayViewSet(ActionBasedPermissionMixin, viewsets.ModelViewSet):
    serializer_class = PlayListRetrieveSerializer
    queryset = Play.objects.prefetch_related("actors", "genres")
    action_serializer_classes = {
        "create": PlayListCreateSerializer,
        "retrieve": PlayDetailSerializer,
        "update": PlayListCreateSerializer,
        "partial_update": PlayListCreateSerializer,
    }
    action_permission_classes = {
        "create": [IsAdminUser],
        "update": [IsAdminUser],
        "partial_update": [IsAdminUser],
        "destroy": [IsAdminUser],
        "list": [IsAuthenticatedOrReadOnly],
        "retrieve": [IsAuthenticatedOrReadOnly],
    }

    def get_serializer_class(self):
        return self.action_serializer_classes.get(self.action, self.serializer_class)


class TheaterHallViewSet(ActionBasedPermissionMixin, viewsets.ModelViewSet):
    serializer_class = TheaterHallSerializer
    queryset = TheaterHall.objects.all()
    action_permission_classes = {
        "create": [IsAdminUser],
        "update": [IsAdminUser],
        "partial_update": [IsAdminUser],
        "destroy": [IsAdminUser],
        "list": [IsAuthenticatedOrReadOnly],
        "retrieve": [IsAuthenticatedOrReadOnly],
    }


class ReservationViewSet(ActionBasedPermissionMixin, viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class PerformanceViewSet(ActionBasedPermissionMixin, viewsets.ModelViewSet):
    serializer_class = PerformanceListSerializer
    queryset = Performance.objects.all()
    action_serializer_classes = {
        "create": PerformanceCreateSerializer,
        "retrieve": PerformanceDetailSerializer,
        "update": PerformanceCreateSerializer,
        "partial_update": PerformanceCreateSerializer,
    }
    action_permission_classes = {
        "create": [IsAdminUser],
        "update": [IsAdminUser],
        "partial_update": [IsAdminUser],
        "destroy": [IsAdminUser],
    }

    def get_queryset(self):
        queryset = super().get_queryset().select_related("theater_hall", "play")
        if self.action == "retrieve":
            return queryset.prefetch_related("play__actors", "play__genres")
        return queryset

    def get_serializer_class(self):
        return self.action_serializer_classes.get(self.action, self.serializer_class)


class TicketViewSet(ActionBasedPermissionMixin, viewsets.ModelViewSet):
    serializer_class = TicketListSerializer
    queryset = Ticket.objects.select_related(
        "performance__play", "reservation", "performance__theater_hall"
    )
    action_serializer_classes = {
        "create": TicketCreateSerializer,
        "retrieve": TicketDetailSerializer,
        "update": TicketCreateSerializer,
        "partial_update": TicketCreateSerializer,
    }
    action_permission_classes = {
        "list": [IsAuthenticatedOrReadOnly],
        "retrieve": [IsAuthenticatedOrReadOnly],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "retrieve":
            return queryset.prefetch_related(
                "performance__play__actors", "performance__play__genres"
            )
        return queryset

    def get_serializer_class(self):
        return self.action_serializer_classes.get(self.action, self.serializer_class)
