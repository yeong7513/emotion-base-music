import os, logging, asyncio, aiohttp
from fastapi import HTTPException
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load YouTube API key from environment variables
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
      raise ValueError("YOUTUBE_API_KEY encironment variable is not set.")

async def is_embeddable(video_ids: List[str]) -> Dict[str, bool]:
      """
      Check whether multiple YouTube videos can be embedded.
      
      :param video_ids: List of YouTube video IDs
      :return: Dictionary with video IDs as keys and boolean values indicating embeddability
      """
      async with aiohttp.ClientSession() as session:
            tasks = [
                  asyncio.create_task(session.get(
                        f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
                  )) for vid in video_ids
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

      return {video_id: (res.status == 200) if isinstance(res, aiohttp.ClientResponse) else False
              for video_id, res in zip(video_ids, results)}

async def youtube_search(query: str, max_results: int = 15) -> List[Dict]:
      """
      Search YouTube for music-related videos.
      
      :param query: Search keyword
      :param max_results: Maximum number of search results to retrieve (default: 15)
      :return: List of dictionaries containing video details
      """
      search_url = (
            f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}"
            f"&key={YOUTUBE_API_KEY}&maxResults={max_results}&type=video&videoCategoryId=10"
      )

      try:
            async with aiohttp.ClientSession() as session:
                  async with session.get(search_url) as response:
                        response.raise_for_status()
                        data = await response.json()

            video_info = {}
            for item in data.get("items", []):
                  video_id = item.get("id", {}).get("videoId")
                  title = item.get("snippet", {}).get("title")
                  thumbnail = item.get("snippet", {}).get("thumbnails", {}).get("default", {}).get("url")

                  if video_id and title:
                        video_info[video_id] = {"title": title, "thumbnail": thumbnail}
      
            # Check which videos are embeddable
            embeddable_dict = await is_embeddable(list(video_info.keys()))

            # Filter videos that are embeddable
            videos = [
                  {
                        "title": info["title"],
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "thumbnail": info["thumbnail"],
                        "video_id": video_id,
                  }
                  for video_id, info in video_info.items()
                  if embeddable_dict.get(video_id)
            ]

            logging.info(f"Final number of videos returned: {len(videos)}")
            return videos

      except aiohttp.ClientResponseError as e:
            logging.error(f"YouTube API request error: {e}")
            raise HTTPException(status_code= e.status, detail= f"YouTube API request error: {e}")
      except (KeyError, TypeError) as e:
            logging.error(f"JSON parsing error: {e}")
            raise HTTPException(status_code= 500, detail=f"JSON parsing error: {e}")
      except Exception as e:
            logging.error(f"Unexpected server error: {e}")
            raise HTTPException(status_code= 500, detail=f"Internal server error: {e}")
      
