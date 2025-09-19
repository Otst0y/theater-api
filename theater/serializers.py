from rest_framework import serializers

from theater.models import Actor, Genre, Play, TheaterHall, Reservation


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

    class Meta:
        model = Play
        fields = ["id", "title", "description", "actors", "genres"]


class PlayDetailSerializer(PlayListCreateSerializer):
    description = serializers.CharField()
    actors = ActorDetailSerializer(many=True, read_only=False)
    genres = GenreSerializer(many=True, read_only=False)

    class Meta:
        model = Play
        fields = ["id", "title", "description", "actors", "genres"]


class TheaterHallSerializer(serializers.ModelSerializer):

    class Meta:
        model = TheaterHall
        fields = ["id", "name", "rows", "seats_in_row", "total_seats"]


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "user"]
