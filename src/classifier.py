from fastapi import APIRouter, HTTPException, status

from src.redis import GetRedis
from src.schemas import ScoreRequest
from src.classifier_service import create_request, get_request

router = APIRouter(prefix="/score")


@router.post("/")
async def score(score_request: ScoreRequest, redis: GetRedis):
    request_id = await create_request(score_request, redis)
    return {"request_id": request_id}


@router.get("/result")
async def result(request_id: str, redis: GetRedis):
    request_data = await get_request(request_id, redis)

    if not request_data:
        raise HTTPException(
            status_code=404,
            detail=f"request with request_id: {request_id} does not exist",
        )

    return request_data
