import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from habits.models import Habit

User = get_user_model()


@pytest.mark.django_db
def test_user_can_create_habit():
    # Тест CRUD своих привычек
    user = User.objects.create_user(username="u1", password="12345")
    client = APIClient()
    client.force_authenticate(user=user)

    payload = {
        "place": "дом",
        "time": "19:00:00",
        "action": "читать 2 страницы",
        "is_pleasant": False,
        "related_habit": None,
        "periodicity": 1,
        "reward": "чай",
        "execution_time": 120,
        "is_public": False,
    }

    resp = client.post("/api/habits/", payload, format="json")
    assert resp.status_code == 201
    assert Habit.objects.filter(owner=user).count() == 1


@pytest.mark.django_db
def test_validator_reward_and_related_habit_conflict():
    # Тест: валидатор reward + related_habit = нельзя
    user = User.objects.create_user(username="u1", password="12345")
    pleasant = Habit.objects.create(
        owner=user,
        place="дом",
        time="18:00:00",
        action="ванна",
        is_pleasant=True,
        periodicity=1,
        execution_time=60,
        is_public=False,
    )

    client = APIClient()
    client.force_authenticate(user=user)

    payload = {
        "place": "улица",
        "time": "19:00:00",
        "action": "прогулка",
        "is_pleasant": False,
        "related_habit": pleasant.id,
        "periodicity": 1,
        "reward": "десерт",
        "execution_time": 60,
        "is_public": False,
    }

    resp = client.post("/api/habits/", payload, format="json")
    assert resp.status_code == 400
