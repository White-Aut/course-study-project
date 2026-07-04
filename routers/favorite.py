from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from crud import favorite
from config.db_conf import get_db
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from schemas.favorite import FavoriteAddRequest, FavoriteCheckResponse, FavoriteListResponse



router = APIRouter(prefix="/api/favorite",tags=["favorite"])


@router.get("/check")
async def check_favorite(
        news_id: int = Query(..., alias="newId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    is_favorited = await favorite.is_news_favorite(db, user.id, news_id)
    return success_response(message="成功", data=FavoriteCheckResponse(isFavorited=is_favorited).data())



@router.post("/add")
async def add_favorite(
        data: FavoriteAddRequest, 
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await favorite.add_favorite(db, user.id, data.news_id)
    return success_response(message="收藏成功", data = result)



@router.delete("/remove")
async def remove_favorite(
        news_id: int = Query(..., alias="newId"), 
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await favorite.remove_favorite(db, user.id, news_id)
    if not result: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="取消收藏失败")
    return success_response(message="取消收藏成功")



@router.get("/list")
async def get_favorite_list(
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, alias="pageSize", le=100, ge = 1, description="每页数量"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    rows,total = await favorite.get_favorite_list(db, user.id, page, page_size)
    favorite_list = []
    for news, favorite_time, favorite_id in rows:
        item = {
            "id": news.id, "title": news.title, "description": news.description or "",
            "image": news.image or "", "author": news.author or "",
            "category_id": news.category_id, "views": news.views or 0,
            "publish_time": news.publish_time.isoformat() if news.publish_time else "",
            "favoriteTime": favorite_time.isoformat() if favorite_time else "",
            "favoriteId": favorite_id
        }
        favorite_list.append(item)
    has_more = total > page * page_size
    data = FavoriteListResponse(hasMore=has_more, total = total, list=favorite_list)
    return success_response(message="获取成功",data = data)



@router.delete("/clear")
async def clear_favorite(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await favorite.remove_all_favorites(db, user.id)
    return success_response(message=f"清空{result}条记录")



