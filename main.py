from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from downloader import fetch_tiktok_video, normalize_url

app = FastAPI(title="TikTok Downloader API", version="1.0.0")

# --- Bagian Baru: Izin Akses (CORS) ---
# Ini supaya Frontend HTML kamu diizinkan mengambil data dari Backend ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua website mengakses API ini
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua metode (GET, POST, dll)
    allow_headers=["*"],  # Mengizinkan semua header
)
# --------------------------------------

@app.get("/")
def home():
    return {"status": "running", "message": "TikTok Downloader API"}


@app.get("/api/info")
async def info(url: str = Query(..., description="TikTok URL")):
    real_url = normalize_url(url)
    data = await fetch_tiktok_video(real_url)

    if "error" in data:
        return JSONResponse({"success": False, "error": data["error"]}, status_code=400)

    return {"success": True, "data": data}

@app.get("/api/download")
async def download(url: str, no_wm: bool = False, audio: bool = False):
    real_url = normalize_url(url)
    data = await fetch_tiktok_video(real_url)

    if "error" in data:
        return JSONResponse({"success": False, "error": data["error"]}, status_code=400)

    if audio:
        return RedirectResponse(data["music"])

    return RedirectResponse(data["video_no_wm"] if no_wm else data["video_wm"])