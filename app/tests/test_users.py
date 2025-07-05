import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_follow_user(client, db):
    """Тест подписки пользователей друг на друга"""
    follow_res_1 = await client.post(
        f"/api/users/2/follow",
        headers={"api-key": "test"}
    )
    follow_res_2 = await client.post(
        f"/api/users/1/follow",
        headers={"api-key": "admin"}
    )
    assert follow_res_1.status_code == 200
    assert follow_res_1.json()["result"] is True
    assert follow_res_2.status_code == 200
    assert follow_res_2.json()["result"] is True


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_profile(client):
    """Тест получения профиля текущего пользователя"""
    response = await client.get(
        "/api/users/me",
        headers={"api-key": "test"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert data["user"]["name"] == "test"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_other_user_profile(client, db):
    """Тест получения профиля другого пользователя"""
    response = await client.get(
        f"/api/users/2",
        headers={"api-key": "test"}
    )
    assert response.status_code == 200
    assert response.json()["user"]["name"] == "admin"
