from rest_framework import routers

from theater.views import (
    ActorViewSet,
    GenreViewSet,
    PlayViewSet,
    TheaterHallViewSet,
    ReservationViewSet,
    PerformanceViewSet,
)

app_name = "theater"

router = routers.DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("plays", PlayViewSet)
router.register("theater_halls", TheaterHallViewSet)
router.register("reservations", ReservationViewSet)
router.register("performances", PerformanceViewSet)

urlpatterns = router.urls
