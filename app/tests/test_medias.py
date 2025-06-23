from io import BytesIO
import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_upload_media(client, test_user):
    """Тест загрузки медиафайла"""
    test_file = BytesIO(b"fake image data")
    test_file.name = "test.jpg"

    response = await client.post(
        "/api/medias",
        files={"file": ("test.jpg", test_file, "image/jpeg")},
        headers={"api-key": "test-key"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["result"] is True
    assert isinstance(data["media_id"], int)
