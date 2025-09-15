from rest_framework import routers

from theater.views import ActorViewSet, GenreViewSet

app_name = "theater"

router = routers.DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)

urlpatterns = router.urls