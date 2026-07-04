from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NewsItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(..., alias="categoryId")
    views: int
    publish_time: Optional[datetime] = Field(..., alias="publishTime")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True    
    )


class NewsItemResponse(NewsItemBase):
    """新闻列表项响应，被 news / favorite 模块共用"""
    pass