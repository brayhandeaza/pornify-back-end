from helpers import xxxbule, pornwhite, vikiporn, pornicom, pervclips, SOURCES
import random
import base64
import ast
from fastapi import APIRouter, Query
from cachetools import TTLCache
from fastapi.responses import JSONResponse

router = APIRouter()
cache = TTLCache(ttl=60 * 10, maxsize=1000)


@router.get("/")
async def get_videos(limit=Query(100)):
    if "videos" in cache:
        return cache["videos"]

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

    vikiporn_videos = vikiporn.all(search, "category")
    xxxbule_videos = xxxbule.all(search, "category")
    pornwhite_videos = pornwhite.all(search, "category")
    pornicom_videos = pornicom.all(search, "category")
    pervclips_videos = pervclips.all(search, "category")

    results = pornicom_videos + vikiporn_videos + \
        xxxbule_videos + pornwhite_videos + pervclips_videos
    random.shuffle(results)

    videos = {
        "status": 200,
        "count": len(results[:int(limit)]),
        "data": results[:int(limit)]
    }

    cache[search] = videos
    return videos


@router.get("/play")
async def get_video_to_play(id=Query(None), title_id=Query(None)):
    if id is None or title_id is None:
        return {
            "status": 404,
            "data": {},
            "error": True,
            "message": f"{id} and {title_id} are required fields"
        }
    decoded_string = None
    try:
        decoded_string = base64.b64decode(f"{id}==")
        my_list = ast.literal_eval(decoded_string.decode('utf-8'))
    except:
        return JSONResponse({
            "status": 400,
            "data": {},
            "error": True
        }, status_code=200)

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
        video = pornwhite.one(box_id, video_id, title_id)
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

    elif (SOURCES[source_id] == "pornicom" and bool(title_id)):
        video = pornicom.one(box_id, video_id, title_id)
        if bool(video) == True:
            return {
                "status": 200,
                "data": video,
                "error": True
            }

    elif (SOURCES[source_id] == "pervclips" and bool(title_id)):
        video = pervclips.one(box_id, video_id, title_id)
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
