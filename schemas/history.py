from pydantic import BaseModel, ConfigDict, Field

from schemas.base import NewsItemResponse



class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newId")

    model_config = ConfigDict(populate_by_name=True)



class HistoryNewsItemResponse(NewsItemResponse):
    viewed_time: str = Field(alias="viewedTime")
    history_id: int = Field(alias="historyId")
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )



class HistoryListResponse(BaseModel):
    list: list[HistoryNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
