import asyncio
import os
import re
import random
import aiohttp
import yt_dlp
from typing import Union
from pathlib import Path

# Aapke bot ke folder structure ke hisaab se imports
from anony import logger
from anony.helpers import Track, utils

try:
    from py_yt import VideosSearch, Playlist
except ImportError:
    from youtubesearchpython.__future__ import VideosSearch, Playlist

# Nayi API Configuration
API_URL = "https://shrutibots.site"

async def download_from_api(link: str, mode: str = "audio") -> str:
    """Shruti API se song ya video download karne ka helper function"""
    video_id = link.split('v=')[-1].split('&')[0] if 'v=' in link else link
    if not video_id or len(video_id) < 3:
        return None

    DOWNLOAD_DIR = "downloads"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    ext = "mp3" if mode == "audio" else "mp4"
    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.{ext}")

    if os.path.exists(file_path):
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": video_id, "type": mode}
            async with session.get(f"{API_URL}/download", params=params, timeout=7) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                token = data.get("download_token")
                if not token:
                    return None
                
                stream_url = f"{API_URL}/stream/{video_id}?type={mode}&token={token}"
                async with session.get(stream_url, timeout=600) as file_resp:
                    # Handle Redirects
                    target_url = file_resp.headers.get('Location') if file_resp.status == 302 else stream_url
                    
                    if file_resp.status in [200, 302]:
                        curr_url = target_url if file_resp.status == 302 else stream_url
                        async with session.get(curr_url) as final_resp:
                            with open(file_path, "wb") as f:
                                async for chunk in final_resp.content.iter_chunked(16384):
                                    f.write(chunk)
                        return file_path if os.path.getsize(file_path) > 0 else None
    except Exception as e:
        logger.error(f"API Download Error: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)
    return None

class YouTube:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = re.compile(
            r"(https?://)?(www\.|m\.|music\.)?"
            r"(youtube\.com/(watch\?v=|shorts/|playlist\?list=)|youtu\.be/)"
            r"([A-Za-z0-9_-]{11}|PL[A-Za-z0-9_-]+)([&?][^\s]*)?"
        )

    def valid(self, url: str) -> bool:
        return bool(re.match(self.regex, url))

    async def search(self, query: str, m_id: int, video: bool = False) -> Track | None:
        try:
            _search = VideosSearch(query, limit=1)
            results = await _search.next()
            if results and results["result"]:
                data = results["result"][0]
                return Track(
                    id=data.get("id"),
                    channel_name=data.get("channel", {}).get("name"),
                    duration=data.get("duration"),
                    duration_sec=utils.to_seconds(data.get("duration")),
                    message_id=m_id,
                    title=data.get("title")[:25],
                    thumbnail=data.get("thumbnails", [{}])[-1].get("url").split("?")[0],
                    url=data.get("link"),
                    view_count=data.get("viewCount", {}).get("short"),
                    video=video,
                )
        except Exception as e:
            logger.error(f"Search Error: {e}")
        return None

    async def playlist(self, limit: int, user: str, url: str, video: bool) -> list:
        tracks = []
        try:
            plist = await Playlist.get(url)
            for data in plist["videos"][:limit]:
                track = Track(
                    id=data.get("id"),
                    channel_name=data.get("channel", {}).get("name", ""),
                    duration=data.get("duration"),
                    duration_sec=utils.to_seconds(data.get("duration")),
                    title=data.get("title")[:25],
                    thumbnail=data.get("thumbnails")[-1].get("url").split("?")[0],
                    url=data.get("link").split("&list=")[0],
                    user=user,
                    view_count="",
                    video=video,
                )
                tracks.append(track)
        except Exception as e:
            logger.error(f"Playlist Error: {e}")
        return tracks

    async def download(self, video_id: str, video: bool = False):
        """Ye function ab Shrutibots API use karega fast download ke liye"""
        url = self.base + video_id
        mode = "video" if video else "audio"
        
        # API se download attempt karein
        downloaded_file = await download_from_api(url, mode=mode)
        
        if downloaded_file:
            return downloaded_file
        
        # Agar API fail ho jaye, toh Backup yt-dlp use karein
        logger.info("API failed, falling back to yt-dlp...")
        ext = "mp4" if video else "webm"
        filename = f"downloads/{video_id}.{ext}"
        
        ydl_opts = {
            "outtmpl": f"downloads/%(id)s.%(ext)s",
            "quiet": True,
            "geo_bypass": True,
            "format": "bestvideo+bestaudio/best" if video else "bestaudio/best",
        }

        def _ydl_download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return filename

        return await asyncio.to_thread(_ydl_download)
        
