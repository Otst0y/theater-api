from rest_framework import routers

from theater.views import ActorViewSet, GenreViewSet, PlayViewSet

app_name = "theater"

router = routers.DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("plays", PlayViewSet)

urlpatterns = router.urls