import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_create_tweet_without_media(client):
    """Тест создания твита без медиа"""
    response = await client.post(
        "/api/tweets",
        json={"tweet_data": "First tweet!"},
        headers={"api-key": "test"}
    )
    assert response.status_code == 201
    assert response.json()["result"] is True


@pytest.mark.asyncio(loop_scope="session")
async def test_create_tweet_with_media(client):
    """
    Тест создания твита с медиа.
    """
    response = await client.post(
        "/api/tweets",
        json={
            "tweet_data": "O kak!",
            "tweet_media_ids": [1]
        },
        headers={"api-key": "admin"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["result"] is True


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_tweet(client, test_user):
    """Тест удаления твита"""
    create_res = await client.post(
        "/api/tweets",
        json={"tweet_data": "To be deleted"},
        headers={"api-key": "test"}
    )
    tweet_id = create_res.json()["tweet_id"]

    delete_res = await client.delete(
        f"/api/tweets/{tweet_id}",
        headers={"api-key": "test"}
    )
    assert delete_res.status_code == 200
    assert delete_res.json()["result"] is True


@pytest.mark.asyncio(loop_scope="session")
async def test_like_unlike_tweet(client, test_user):
    """Тест добавления лайка"""
    tweet_res = await client.post(
        "/api/tweets",
        json={"tweet_data": "To like"},
        headers={"api-key": "test"}
    )

    tweet_id = tweet_res.json()["tweet_id"]

    like_res = await client.post(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": "admin"}
    )
    assert like_res.status_code == 201
    assert like_res.json()["result"] is True
