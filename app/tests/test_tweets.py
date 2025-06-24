from db import User, Follow, Tweet
import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_create_tweet_without_media(client, test_user):
    """Тест создания твита без медиа"""
    response = await client.post(
        "/api/tweets",
        json={"tweet_data": "Test tweet content"},
        headers={"api-key": "test-key"}
    )
    assert response.status_code == 201
    assert response.json()["result"] is True


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_tweet(client, test_user):
    """Тест удаления твита"""
    create_res = await client.post(
        "/api/tweets",
        json={"tweet_data": "To be deleted"},
        headers={"api-key": "test-key"}
    )
    tweet_id = create_res.json()["tweet_id"]

    delete_res = await client.delete(
        f"/api/tweets/{tweet_id}",
        headers={"api-key": "test-key"}
    )
    assert delete_res.status_code == 200
    assert delete_res.json()["result"] is True


@pytest.mark.asyncio(loop_scope="session")
async def test_like_unlike_tweet(client, test_user):
    """Тест добавления и удаления лайка"""
    tweet_res = await client.post(
        "/api/tweets",
        json={"tweet_data": "To like"},
        headers={"api-key": "test-key"}
    )
    tweet_id = tweet_res.json()["tweet_id"]

    like_res = await client.post(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": "test-key"}
    )
    assert like_res.status_code == 201
    assert like_res.json()["result"] is True

    unlike_res = await client.delete(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": "test-key"}
    )
    assert unlike_res.status_code == 200
    assert unlike_res.json()["result"] is True


@pytest.mark.asyncio(loop_scope="session")
async def test_get_feed(client, db, test_user):
    """Тест получения ленты твитов"""
    author = User(name="Author", api_key="author-key")
    db.add(author)
    await db.commit()

    follow = Follow(follower_id=test_user.id, following_id=author.id)
    db.add(follow)

    tweet = Tweet(user_id=author.id, content="Test feed content")
    db.add(tweet)
    await db.commit()

    feed_res = await client.get(
        "/api/tweets",
        headers={"api-key": "test-key"}
    )
    assert feed_res.status_code == 200
    data = feed_res.json()
    assert data["result"] is True
    assert len(data["tweets"]) == 1
    assert data["tweets"][0]["content"] == "Test feed content"
