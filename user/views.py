from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer

User = get_user_model()


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = ()


class LoginUserView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class ManageUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
