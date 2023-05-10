# from fastapi import APIRouter, Query
# from config.database import engine
# from models.Tags import Tags

# items = APIRouter()


# @items.get("")
# async def get_items():
#     with engine.begin() as conn:
#         items = conn.execute(Tags.__table__.select()).all()
#     return items


# @items.get("/search")
# async def get_items(q=Query(None)):

#     if q == None:
#         return {
#             "status": 422,
#             "message": "Unprocessable Entity: q param is required",
#         }

#     with engine.begin() as conn:
#         data = conn.execute(
#             Tags.__table__.select().where(
#                 Tags.title.ilike(f"%{q}%")
#             ).limit(10)
#         ).all()

#     return {
#         "status": 200,
#         "count": len(data),
#         "data": data
#     }
