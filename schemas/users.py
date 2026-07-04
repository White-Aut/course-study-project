from typing import Optional

from pydantic import BaseModel, Field, ConfigDict



class UserRequest(BaseModel):
    username: str
    password: str



class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")



class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    model_config = ConfigDict(
        from_attributes = True
    )


    


class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")
    model_config = ConfigDict(
        populate_by_name = True,
        from_attributes = True
    )

    def data(self):
        return self.model_dump(by_alias=True)



class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
    )




class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(..., alias = "oldPassword", description="Old password")
    new_password: str = Field(..., min_length = 6, alias = "newPassword", description="New password")