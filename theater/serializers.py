from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField

from theater.models import (
    Actor,
    Genre,
    Play,
    TheaterHall,
    Reservation,
    Performance,
    Ticket,
)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name"]


class ActorDetailSerializer(ActorSerializer):
    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name", "full_name"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class PlayListRetrieveSerializer(serializers.ModelSerializer):
    description = serializers.CharField(write_only=True)
    short_description = serializers.SerializerMethodField()
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Play
        fields = ["id", "title", "description", "short_description", "actors", "genres"]

    def get_short_description(self, obj):
        if len(obj.description) > 75:
            return obj.description[:75] + "..."
        return obj.description


class PlayListCreateSerializer(PlayListRetrieveSerializer):
    actors = serializers.PrimaryKeyRelatedField(many=True, queryset=Actor.objects.all())
    genres = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all())


class PlayDetailSerializer(PlayListCreateSerializer):
    description = serializers.CharField()
    actors = ActorDetailSerializer(many=True, read_only=False)
    genres = GenreSerializer(many=True, read_only=False)


class TheaterHallSerializer(serializers.ModelSerializer):

    class Meta:
        model = TheaterHall
        fields = ["id", "name", "rows", "seats_in_row", "total_seats"]


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "user"]


class PerformanceListSerializer(serializers.ModelSerializer):
    play = serializers.SlugRelatedField(read_only=True, slug_field="title")
    theater_hall = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Performance
        fields = ["id", "play", "theater_hall", "show_time"]


class PerformanceCreateSerializer(PerformanceListSerializer):
    play = serializers.PrimaryKeyRelatedField(queryset=Play.objects.all())
    theater_hall = serializers.PrimaryKeyRelatedField(
        queryset=TheaterHall.objects.all()
    )


class PerformanceDetailSerializer(PerformanceListSerializer):
    play = PlayDetailSerializer(read_only=True)
    theater_hall = TheaterHallSerializer(read_only=True)


class TicketListSerializer(serializers.ModelSerializer):
    play_title = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "play_title", "reservation"]

    def get_play_title(self, obj):
        return obj.performance.play.title


class TicketCreateSerializer(TicketListSerializer):
    performance = PrimaryKeyRelatedField(queryset=Performance.objects.all())

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance", "reservation"]

    def validate(self, attrs):
        row = attrs["row"]
        seat = attrs["seat"]
        performance = attrs["performance"]

        hall = performance.theater_hall

        if row > hall.rows:
            raise serializers.ValidationError(
                f"The row must be between 1 and {hall.rows}"
            )

        if seat > hall.seats_in_row:
            raise serializers.ValidationError(
                f"The seat must be between 1 and {hall.seats_in_row}"
            )

        if Ticket.objects.filter(performance=performance, row=row, seat=seat).exists():
            raise serializers.ValidationError(
                "The seat is already taken. Please chose another one."
            )

        return attrs

    def create(self, validated_data):
        try:
            return super().create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "This seat just been booked by someone else. Please chose another one."
            )


class TicketDetailSerializer(TicketListSerializer):
    performance = PerformanceDetailSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance", "reservation"]
