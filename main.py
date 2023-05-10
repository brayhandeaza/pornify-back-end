from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.videos import router as videos_router, update_cache
from routes.tags import items as items_router
from sqlmodel import SQLModel
from config.database import engine
from apscheduler.schedulers.background import BackgroundScheduler
from helpers import xxxbule, pornwhite, vikiporn, pornicom, pervclips
import random

app = FastAPI()
scheduler = BackgroundScheduler()
SQLModel.metadata.create_all(engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup_event():
    with engine.begin() as conn:
        pass


app.include_router(videos_router, prefix="/videos")
app.include_router(items_router, prefix="/items")


def call_my_route():
    vikiporn_videos = vikiporn.all("")
    xxxbule_videos = xxxbule.all("")
    pornwhite_videos = pornwhite.all("")
    pornicom_videos = pornicom.all("")
    pervclips_videos = pervclips.all("")

    results = pornicom_videos + vikiporn_videos + \
        xxxbule_videos + pornwhite_videos + pervclips_videos
    random.shuffle(results)

    videos = {
        "status": 200,
        "count": len(results[:int(100)]),
        "data": results[:int(100)]
    }

    update_cache(videos)


scheduler.add_job(call_my_route, 'interval', seconds=60 * 9)
scheduler.start()


@app.get("/{path:path}")
async def catch_all(path: str):
    return {"message": f"Endpoint {path} not found"}
