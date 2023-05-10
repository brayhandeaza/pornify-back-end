from fastapi import APIRouter, Query
# from config.database import engine
# from models.Tags import Tags
from helpers import TAGS

tags = APIRouter()


@tags.get("")
async def get_tags():
    return {
        "status": 200,
        "count": len(TAGS),
        "data": TAGS
    }


@tags.get("/search")
async def get_tags(query=Query(None)):
    data = [tag for tag in TAGS if query in tag][:10]

    return {
        "status": 200,
        "count": len(data),
        "data": data
    }
