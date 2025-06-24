from db import User
import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_follow_unfollow_user(client, db, test_user):
    """Тест подписки и отписки от пользователя"""
    user2 = User(name="User2", api_key="key2")
    db.add(user2)
    await db.commit()

    follow_res = await client.post(
        f"/api/users/{user2.id}/follow",
        headers={"api-key": "test-key"}
    )
    assert follow_res.status_code == 200
    assert follow_res.json()["result"] is True

    unfollow_res = await client.delete(
        f"/api/users/{user2.id}/follow",
        headers={"api-key": "test-key"}
    )
    assert unfollow_res.status_code == 200
    assert unfollow_res.json()["result"] is True


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_profile(client, test_user):
    """Тест получения профиля текущего пользователя"""
    response = await client.get(
        "/api/users/me",
        headers={"api-key": "test-key"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert data["user"]["name"] == "TestUser"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_other_user_profile(client, db, test_user):
    """Тест получения профиля другого пользователя"""
    user3 = User(name="User3", api_key="key3")
    db.add(user3)
    await db.commit()

    response = await client.get(
        f"/api/users/{user3.id}",
        headers={"api-key": "test-key"}
    )
    assert response.status_code == 200
    assert response.json()["user"]["name"] == "User3"
