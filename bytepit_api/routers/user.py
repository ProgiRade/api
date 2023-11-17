import base64

from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.responses import FileResponse

from bytepit_api.dependencies.auth_dependencies import get_current_verified_user
from bytepit_api.models.auth_schemes import User


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/current", response_model=User)
def get_current_user(current_user: Annotated[User, Depends(get_current_verified_user)]):
    return current_user
