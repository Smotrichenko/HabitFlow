import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from habits.models import Habit

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_1(db):
    return User.objects.create_user(
        username="user1", password="12345", telegram_chat_id="111"
    )


@pytest.fixture
def user_2(db):
    return User.objects.create_user(
        username="user2", password="12345", telegram_chat_id="222"
    )


@pytest.fixture
def pleasant_habit(user_1):
    # приятная привычка (для валидаторов)
    return Habit.objects.create(
        owner=user_1,
        place="дом",
        time="18:00:00",
        action="принять ванну",
        is_pleasant=True,
        periodicity=1,
        execution_time=60,
        is_public=False,
    )
