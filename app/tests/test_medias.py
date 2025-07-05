import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_upload_media(client):
    """Тест загрузки медиафайла"""

    media_path = "media/cat.png"
    with open(media_path, "rb") as file:
        response = await client.post(
            "/api/medias",
            files={"file": ("cat.png", file, "image/png")},
            headers={"api-key": "admin"}
        )
    assert response.status_code == 201
    data = response.json()
    assert data["result"] is True
    assert isinstance(data["media_id"], int)
