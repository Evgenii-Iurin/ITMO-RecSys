from typing import List
from enum import Enum

from fastapi import APIRouter, FastAPI, Path, Request
from pydantic import BaseModel

from service.api.exceptions import ModelNotFoundError, UserNotFoundError
from service.log import app_logger


class ModelName(str, Enum):
    TEST = "test_model"
    MOCK = "mock_model"

class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


router = APIRouter()


@router.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    return "I am alive"


@router.get(
    path="/reco/{model_name}/{user_id}",
    tags=["Recommendations"],
    response_model=RecoResponse,
)
async def get_reco(
    request: Request,
    model_name: str,
    user_id: int,
) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")

    try:
        ModelName(model_name)
    except ValueError:
        raise ModelNotFoundError(
            error_message=f"Model {model_name} not found. Available models: {[m.value for m in ModelName]}"
        )

    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    k_recs = request.app.state.k_recs
    reco = list(range(k_recs))
    return RecoResponse(user_id=user_id, items=reco)


def add_views(app: FastAPI) -> None:
    app.include_router(router)
