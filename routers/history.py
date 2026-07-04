
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from crud import history as history_crud
from config.db_conf import get_db
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from schemas.history import HistoryAddRequest, HistoryListResponse



router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_history(
        data: HistoryAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await history_crud.add_history(db, user.id, data.news_id)
    return success_response(message="添加浏览历史成功", data=result)



@router.get("/list")
async def get_history_list(
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, alias="pageSize", le=100, ge=1, description="每页数量"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    rows, total = await history_crud.get_history_list(db, user.id, page, page_size)
    history_list = []
    for news, viewed_time, history_id in rows:
        item = {
            "id": news.id, "title": news.title, "description": news.description or "",
            "image": news.image or "", "author": news.author or "",
            "category_id": news.category_id, "views": news.views or 0,
            "publish_time": news.publish_time.isoformat() if news.publish_time else "",
            "viewedTime": viewed_time.isoformat() if viewed_time else "",
            "historyId": history_id
        }
        history_list.append(item)
    has_more = total > page * page_size
    data = HistoryListResponse(hasMore=has_more, total=total, list=history_list)
    return success_response(message="获取浏览历史成功", data=data)


@router.delete("/remove")
async def remove_history(
        history_id: int = Query(..., alias="historyId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await history_crud.remove_history(db, user.id, history_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="删除浏览历史失败")
    return success_response(message="删除浏览历史成功")



@router.delete("/clear")
async def clear_all_history(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    count = await history_crud.clear_all_history(db, user.id)
    return success_response(message=f"清空{count}条浏览历史")