from typing import List

from pydantic import ConfigDict, Field

from schemas.base import NewsItemBase, NewsItemResponse


class NewsDetailResponse(NewsItemBase):
    """新闻详情响应"""
    content: str
    related_news: List[NewsItemResponse] = Field(default_factory=list, alias="relatedNews")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
