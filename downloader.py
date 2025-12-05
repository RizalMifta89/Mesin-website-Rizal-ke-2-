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
    Fungsi backend simpel.
    NOTE: TikTok TIDAK menyediakan API publik, jadi downloader memakai scraping endpoint.
    Di sini kita gunakan endpoint pihak ketiga (tanpa API key) hanya untuk demo.
    Kamu bebas ganti ke service lain nanti.
    """

    api = "https://www.tikwm.com/api/"  # API publik non-official TikTok

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(api, data={"url": url})
            data = r.json()

        if data.get("code") != 0:
            raise Exception("API gagal memproses link.")

        result = data["data"]

        return {
            "title": result.get("title", ""),
            "author": result.get("author", {}).get("unique_id", "unknown"),
            "duration": result.get("duration", 0),
            "video_no_wm": result.get("play", ""),
            "video_wm": result.get("wmplay", ""),
            "music": result.get("music", ""),
            "cover": result.get("cover", ""),
        }

    except Exception as e:
        return {"error": str(e)}