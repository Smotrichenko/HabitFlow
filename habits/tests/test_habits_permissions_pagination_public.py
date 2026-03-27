import pytest
from habits.models import Habit


@pytest.mark.django_db
def test_user_sees_only_own_habits(api_client, user_1, user_2):
    # Тест: каждый пользователь видит только свои привычки
    Habit.objects.create(
        owner=user_1,
        place="дом",
        time="10:00:00",
        action="привычка 1",
        is_pleasant=False,
        periodicity=1,
        execution_time=60,
        is_public=False,
        reward="чай",
    )
    Habit.objects.create(
        owner=user_2,
        place="дом",
        time="11:00:00",
        action="привычка 2",
        is_pleasant=False,
        periodicity=1,
        execution_time=60,
        is_public=False,
        reward="кофе",
    )

    api_client.force_authenticate(user=user_1)
    resp = api_client.get("/api/habits/")
    assert resp.status_code == 200
    # в выдаче должна быть только 1 привычка user_1
    assert resp.data["count"] == 1


@pytest.mark.django_db
def test_user_cannot_edit_foreign_habit(api_client, user_1, user_2):
    # Тест: нельзя редактировать чужие привычки
    foreign = Habit.objects.create(
        owner=user_2,
        place="дом",
        time="11:00:00",
        action="чужая",
        is_pleasant=False,
        periodicity=1,
        execution_time=60,
        is_public=False,
        reward="кофе",
    )

    api_client.force_authenticate(user=user_1)
    resp = api_client.patch(
        f"/api/habits/{foreign.id}/", {"place": "улица"}, format="json"
    )
    # вернёт 404, потому что queryset фильтруется по owner
    assert resp.status_code == 404


@pytest.mark.django_db
def test_pagination_5_per_page(api_client, user_1):
    # Тест: пагинация по 5
    api_client.force_authenticate(user=user_1)

    for i in range(6):
        Habit.objects.create(
            owner=user_1,
            place="дом",
            time="10:00:00",
            action=f"привычка {i}",
            is_pleasant=False,
            periodicity=1,
            execution_time=60,
            is_public=False,
            reward="чай",
        )

    resp1 = api_client.get("/api/habits/")
    assert resp1.status_code == 200
    assert len(resp1.data["results"]) == 5
    assert resp1.data["next"] is not None

    resp2 = api_client.get(resp1.data["next"])
    assert resp2.status_code == 200
    assert len(resp2.data["results"]) == 1


@pytest.mark.django_db
def test_public_habits_list_allow_any(api_client, user_1, user_2):
    # Тест: список публичных привычек доступен без редактирования
    Habit.objects.create(
        owner=user_1,
        place="парк",
        time="12:00:00",
        action="публичная 1",
        is_pleasant=False,
        periodicity=1,
        execution_time=60,
        is_public=True,
        reward="чай",
    )
    Habit.objects.create(
        owner=user_2,
        place="улица",
        time="13:00:00",
        action="публичная 2",
        is_pleasant=False,
        periodicity=1,
        execution_time=60,
        is_public=True,
        reward="кофе",
    )
    Habit.objects.create(
        owner=user_2,
        place="дом",
        time="14:00:00",
        action="не публичная",
        is_pleasant=False,
        periodicity=1,
        execution_time=60,
        is_public=False,
        reward="кофе",
    )

    # без авторизации
    resp = api_client.get("/api/habits/public/")
    assert resp.status_code == 200
    assert resp.data["count"] == 2

    # попытка POST на публичный список -> 405
    resp_post = api_client.post("/api/habits/public/", {}, format="json")
    assert resp_post.status_code == 405
