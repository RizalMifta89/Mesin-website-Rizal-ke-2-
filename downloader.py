import httpx
import re

# SIMPLE TikTok URL NORMALIZER

def normalize_url(url: str) -> str:
    # Follow redirects if using short URL (vm.tiktok.com)
    try:
        with httpx.Client(follow_redirects=True, timeout=10) as client:
            response = client.get(url)
            return str(response.url)
    except Exception:
        return url


async def fetch_tiktok_video(url: str) -> dict:
    """
    Versi UPGRADE: Memprioritaskan kualitas HD (1080p/720p High Bitrate)
    """

    api = "https://www.tikwm.com/api/" 

    try:
        async with httpx.AsyncClient(timeout=20) as client: # Timeout dinaikkan dikit biar aman
            r = await client.post(api, data={"url": url})
            data = r.json()

        if data.get("code") != 0:
            raise Exception("API gagal memproses link.")

        result = data["data"]

        # LOGIC PENTING: Prioritas HD
        # Kita cek apakah 'hdplay' ada isinya? Jika ada, pakai itu.
        # Jika tidak ada, pakai 'play' biasa.
        final_video_url = result.get("hdplay")
        if not final_video_url:
            final_video_url = result.get("play", "")

        return {
            "title": result.get("title", ""),
            "author": result.get("author", {}).get("unique_id", "unknown"),
            "duration": result.get("duration", 0),
            "video_no_wm": final_video_url, # <--- Ini sekarang otomatis HD
            "video_wm": result.get("wmplay", ""),
            "music": result.get("music", ""),
            "cover": result.get("cover", ""),
            "is_hd": True if result.get("hdplay") else False # Info tambahan (opsional)
        }

    except Exception as e:
        return {"error": str(e)}