from helpers import xxxbule, pornwhite, vikiporn, SOURCES
from flask_caching import Cache
import random
import base64
import ast
from fastapi import APIRouter, Query
from cachetools import TTLCache

router = APIRouter()
cache = TTLCache(ttl=60 * 10, maxsize=1000)


@router.get("/")
async def get_videos(limit=Query(100)):
    if "videos" in cache:
        return cache["videos"]

    vikiporn_videos = vikiporn.all("")
    xxxbule_videos = xxxbule.all("")
    pornwhite_videos = pornwhite.all("")

    results = xxxbule_videos + pornwhite_videos + vikiporn_videos
    random.shuffle(results)

    videos = {
        "status": 200,
        "count": len(results[:int(limit)]),
        "data": results[:int(limit)]
    }

    cache["videos"] = videos
    return videos


@router.get("/category")
async def get_videos_by_catgory(search=Query(None), limit=Query(100)):

    if search == None:
        return {
            "status": 422,
            "message": "Unprocessable Entity: search is require",
        }

    if search in cache:
        return cache[search]

    vikiporn_videos = vikiporn.all(search)
    xxxbule_videos = xxxbule.all(search)
    pornwhite_videos = pornwhite.all(search)

    results = vikiporn_videos + xxxbule_videos + pornwhite_videos
    random.shuffle(results)

    videos = {
        "status": 200,
        "count": len(results[:int(limit)]),
        "data": results[:int(limit)]
    }

    cache[search] = videos
    return videos


@router.get("/play")
async def get_video_to_play(id=Query(), title_id=Query()):
    decoded_string = base64.b64decode(f"{id}==")
    my_list = ast.literal_eval(decoded_string.decode('utf-8'))

    box_id = my_list[0]
    source_id = my_list[1]
    video_id = my_list[2]

    video = None
    if (SOURCES[source_id] == "vikiporn" and bool(title_id) and box_id != "False" and video_id != "False"):
        video = vikiporn.one(box_id, video_id, title_id)
        if bool(video) == True:
            return {
                "status": 200,
                "data": video,
                "error": False
            }

    elif (SOURCES[source_id] == "pornwhite" and bool(title_id) and box_id != "False" and video_id != "False"):
        video = pornwhite.one(video_id, title_id, box_id)
        if bool(video) == True:
            return {
                "status": 404,
                "data": video,
                "error": True
            }

    elif (SOURCES[source_id] == "xxxbule" and bool(title_id)):
        video = xxxbule.one(video_id)
        if bool(video) == True:
            return {
                "status": 200,
                "data": video,
                "error": True
            }

    else:
        return {
            "status": 404,
            "data": {},
            "error": True
        }
