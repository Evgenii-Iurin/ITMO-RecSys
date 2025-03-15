from enum import Enum
from typing import List

from fastapi import APIRouter, FastAPI, Request
from pydantic import BaseModel

from service.api.exceptions import ModelNotFoundError, UserNotFoundError
from service.log import app_logger


class ModelName(str, Enum):
    TEST = "test_model"
    MOCK = "mock_model"


class RecoResponse(BaseModel):
    """
    Response model for recommendations

    Attributes:
        user_id: ID of the user who requested recommendations
        items: List of recommended item IDs
    """

    user_id: int
    items: List[int]


router = APIRouter()


@router.get(
    path="/health",
    tags=["Health"],
    summary="Health check endpoint",
    description="Returns a simple message to confirm the service is running",
    response_description="Returns 'I am alive' if service is healthy",
)
async def health() -> str:
    """
    Simple health check endpoint to verify service is running.

    Returns:
        str: "I am alive" message
    """
    return "I am alive"


@router.get(
    path="/reco/{model_name}/{user_id}",
    tags=["Recommendations"],
    response_model=RecoResponse,
    summary="Get recommendations for a user",
    description="Returns personalized recommendations for a given user using specified model",
    responses={
        200: {
            "description": "Successful response with recommendations",
            "content": {"application/json": {"example": {"user_id": 123, "items": [1, 2, 3, 4, 5]}}},
        },
        404: {
            "description": "User or model not found",
            "content": {
                "application/json": {
                    "example": {
                        "errors": [{"error_key": "model_not_found", "error_message": "Model invalid_model not found"}]
                    }
                }
            },
        },
    },
)
async def get_reco(
    request: Request,
    model_name: str,
    user_id: int,
) -> RecoResponse:
    """
    Get personalized recommendations for a user.

    Args:
        request: FastAPI request object
        model_name: Name of the model to use for recommendations
        user_id: ID of the user to get recommendations for

    Returns:
        RecoResponse: Object containing user ID and list of recommended items

    Raises:
        ModelNotFoundError: If specified model doesn't exist
        UserNotFoundError: If user ID is invalid or not found
    """
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
