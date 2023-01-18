from django.shortcuts import render

from .models import User


def user_check_instance(from_user):
    """Check user data.
    If user not exist register.
    If user exists and data changed, edit data."""

    user = User.objects.filter(tg_id=from_user.id).first()
    if user:
        user_update(user, from_user)
    else:
        user_create(from_user)


def user_create(from_user):
    """Create user."""

    user = User.objects.create(
        tg_id=from_user.id,
        username=from_user.username,
        first_name=from_user.first_name,
        last_name=from_user.last_name,
    )
    user.save()
    #
    print(f"creating {from_user.id}")


def user_update(user, from_user):
    """Update fields if data changed."""

    if user.username != from_user.username:
        User.objects.filter(username=from_user.username).update(username=None)
        user.username = from_user.username
        user.save()
        #
        print(f"updating username {from_user.id}")

    if (
        user.first_name != from_user.first_name
        or user.last_name != from_user.last_name
    ):
        user.first_name = from_user.first_name
        user.last_name = from_user.last_name
        user.save()
        #
        print(f"updating name {from_user.id}")
