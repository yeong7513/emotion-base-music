import os
import pytest
from aioresponses import aioresponses
from dotenv import load_dotenv

from services.youtube_api import is_embeddable, youtube_search

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "test_api_key")

@pytest.mark.asyncio
async def test_is_embeddable():
    video_ids = ["video1", "video2"]

    # Use aioresponses to mock HTTP responses
    with aioresponses() as mocked:  # <-- Используем обычный `with`, так как aioresponses не поддерживает async with.
        url1 = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=video1&format=json"
        mocked.get(url1, status=200, payload={"data": "value"})

        url2 = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=video2&format=json"
        mocked.get(url2, status=404)

        result = await is_embeddable(video_ids)
        assert result["video1"] is True
        assert result["video2"] is False

@pytest.mark.asyncio
async def test_youtube_search():
    query = "music"
    max_results = 2

    search_url = (
        f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}"
        f"&key={YOUTUBE_API_KEY}&maxResults={max_results}&type=video&videoCategoryId=10"
    )

    fake_search_response = {
        "items": [
            {
                "id": {"videoId": "video1"},
                "snippet": {
                    "title": "Test Video 1",
                    "thumbnails": {"default": {"url": "http://example.com/thumb1.jpg"}}
                }
            },
            {
                "id": {"videoId": "video2"},
                "snippet": {
                    "title": "Test Video 2",
                    "thumbnails": {"default": {"url": "http://example.com/thumb2.jpg"}}
                }
            }
        ]
    }

    with aioresponses() as mocked:
        mocked.get(search_url, status=200, payload=fake_search_response)

        url_video1 = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=video1&format=json"
        url_video2 = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=video2&format=json"
        mocked.get(url_video1, status=200, payload={"data": "value"})
        mocked.get(url_video2, status=404)

        videos = await youtube_search(query, max_results)

        assert len(videos) == 1
        video = videos[0]
        assert video["video_id"] == "video1"
        assert video["title"] == "Test Video 1"
        assert video["thumbnail"] == "http://example.com/thumb1.jpg"
        assert video["url"] == "https://www.youtube.com/watch?v=video1"
