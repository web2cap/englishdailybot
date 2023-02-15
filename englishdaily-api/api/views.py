import logging

from django.conf import settings
from rest_framework import mixins
from rest_framework import viewsets

from .serializers import UserSerializer
from users.models import User


MESSAGES = getattr(settings, "MESSAGES", None)


class CreateUpdateRetriveViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Allow create, update, retrive."""

    pass


class UserViewSet(CreateUpdateRetriveViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "tg_id"

    def update(self, request, *args, **kwargs):
        """ "If the username exist in the database, it is not relevant there.
        Foundin username set to None."""

        new_username = request.data.get("username")
        if new_username:
            users_with_username = User.objects.filter(username=new_username)
            if users_with_username.exists():
                user = users_with_username.first()
                tg_id = kwargs.get("tg_id")
                if str(user.tg_id) != tg_id:
                    user.username = None
                    user.save()
                    logging.info(f"{user.tg_id} have unactual username")
        return super().update(request, *args, **kwargs)
