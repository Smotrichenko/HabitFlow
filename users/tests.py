import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_register(api_client):
    # Тест: Регистрация
    payload = {"username": "new_user", "password": "12345", "telegram_chat_id": "999"}
    resp = api_client.post("/api/auth/register/", payload, format="json")
    assert resp.status_code == 201
    assert User.objects.filter(username="new_user").exists()


@pytest.mark.django_db
def test_login_jwt(api_client):
    # Тест: Авторизация JWT
    User.objects.create_user(username="u1", password="12345")
    resp = api_client.post(
        "/api/auth/token/", {"username": "u1", "password": "12345"}, format="json"
    )
    assert resp.status_code == 200
    assert "access" in resp.data
    assert "refresh" in resp.data
