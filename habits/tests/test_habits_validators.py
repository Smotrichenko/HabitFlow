import pytest
from habits.models import Habit


@pytest.mark.django_db
def test_validator_reward_and_related_conflict(api_client, user_1, pleasant_habit):
    # Тест: reward + related_habit = нельзя одновременно
    api_client.force_authenticate(user=user_1)

    payload = {
        "place": "улица",
        "time": "19:00:00",
        "action": "прогулка",
        "is_pleasant": False,
        "related_habit": pleasant_habit.id,
        "periodicity": 1,
        "reward": "десерт",
        "execution_time": 60,
        "is_public": False,
    }

    resp = api_client.post("/api/habits/", payload, format="json")
    assert resp.status_code == 400


@pytest.mark.django_db
def test_validator_execution_time_max_120(api_client, user_1):
    # Тест: execution_time <= 120
    api_client.force_authenticate(user=user_1)

    payload = {
        "place": "дом",
        "time": "10:00:00",
        "action": "отжимания",
        "is_pleasant": False,
        "periodicity": 1,
        "reward": "чай",
        "execution_time": 121,  # нарушаем
        "is_public": False,
    }

    resp = api_client.post("/api/habits/", payload, format="json")
    assert resp.status_code == 400


@pytest.mark.django_db
def test_validator_periodicity_1_to_7(api_client, user_1):
    # Тест: нельзя реже 1 раза в 7 дней
    api_client.force_authenticate(user=user_1)

    payload = {
        "place": "дом",
        "time": "10:00:00",
        "action": "читать",
        "is_pleasant": False,
        "periodicity": 8,  # нарушаем
        "reward": "кофе",
        "execution_time": 60,
        "is_public": False,
    }

    resp = api_client.post("/api/habits/", payload, format="json")
    assert resp.status_code == 400


@pytest.mark.django_db
def test_validator_related_must_be_pleasant(api_client, user_1):
    # Тест: в related_habit только приятные
    api_client.force_authenticate(user=user_1)

    not_pleasant = Habit.objects.create(
        owner=user_1,
        place="дом",
        time="12:00:00",
        action="полезная привычка",
        is_pleasant=False,
        periodicity=1,
        execution_time=60,
        is_public=False,
        reward="чай",
    )

    payload = {
        "place": "улица",
        "time": "19:00:00",
        "action": "прогулка",
        "is_pleasant": False,
        "related_habit": not_pleasant.id,  # нарушаем
        "periodicity": 1,
        "execution_time": 60,
        "is_public": False,
    }

    resp = api_client.post("/api/habits/", payload, format="json")
    assert resp.status_code == 400


@pytest.mark.django_db
def test_validator_pleasant_cannot_have_reward(api_client, user_1):
    # Тест: у приятной привычки не может быть reward
    api_client.force_authenticate(user=user_1)

    payload = {
        "place": "дом",
        "time": "20:00:00",
        "action": "смотреть сериал",
        "is_pleasant": True,
        "periodicity": 1,
        "reward": "конфета",  # нарушаем
        "execution_time": 60,
        "is_public": False,
    }

    resp = api_client.post("/api/habits/", payload, format="json")
    assert resp.status_code == 400
