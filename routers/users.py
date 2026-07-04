from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from schemas.users import UserAuthResponse, UserInfoResponse, UserRequest, UserChangePasswordRequest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from schemas.users import UserUpdateRequest
from config.db_conf import get_db
from crud import users
from models.users import User
from schemas.users import UserAuthResponse, UserInfoResponse, UserRequest
from utils.auth import get_current_user
from utils.response import success_response



router = APIRouter(prefix="/api/user",tags=["users"])



@router.post("/register")
async def register(user_data:UserRequest, db: AsyncSession = Depends(get_db)):

    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)

    response = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data=response.data())



@router.post("/login")
async def login_user(login_data: UserRequest, db: AsyncSession = Depends(get_db)):
    user = await users.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功", data=response_data.data())



@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功", data = UserInfoResponse.model_validate(user))



@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await users.update_user(db, user.username, user_data)
    return success_response(message="更新用户信息成功", data = UserInfoResponse.model_validate(user))



@router.put("/password")
async def update_password(password_data: UserChangePasswordRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res_change_pwd = await users.change_password(db, user, password_data.old_password, password_data.new_password)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="修改失败")
    return success_response(message="更新密码成功")



