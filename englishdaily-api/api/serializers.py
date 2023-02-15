import logging

from django.conf import settings
from rest_framework import serializers

from users.models import User


MESSAGES = getattr(settings, "MESSAGES", None)


class UserSerializer(serializers.ModelSerializer):
    """User Serializer disabled update tg_id.
    Provide unic username it telegram context."""

    def validate_tg_id(self, value):
        current_tg_id = getattr(self.instance, "tg_id", None)
        if current_tg_id and current_tg_id != value:
            raise serializers.ValidationError(
                MESSAGES["tg_id_update_forbidden"]
            )
        return value

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "tg_id",
            "first_name",
            "last_name",
        )
