from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_start.db.session import get_db_session
from test_project.entities.user import UserDTO
from test_project.services.user import UserService
from test_project.repositories.user import UserRepositoryImpl


def get_user_service(session: AsyncSession = Depends(get_db_session)):
    return UserService(UserRepositoryImpl(session))


router = APIRouter()


@router.get("/users", response_model=List[UserDTO])
async def fetch_users(service: UserService = Depends(get_user_service)):
    return await service.list_items()
