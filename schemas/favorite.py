from pydantic import BaseModel, ConfigDict, Field

from schemas.base import NewsItemResponse



class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")



class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newId")

    model_config = ConfigDict(populate_by_name=True)



class FavoriteDeleteRequest(BaseModel):
    news_id: int = Field(..., alias="newId")



class FavoriteNewsItemResponse(NewsItemResponse):
    favorite_id: int = Field(alias="favoriteId")
    favorite_time: str = Field(alias="favoriteTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )



class FavoriteListResponse(BaseModel):
    list:list[FavoriteNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


