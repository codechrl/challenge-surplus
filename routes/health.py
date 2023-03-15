from fastapi import APIRouter, status

from schema.message import BasicMessage

router = APIRouter()


@router.get("", response_model=BasicMessage, status_code=status.HTTP_200_OK)
async def health_test():
    return BasicMessage(message="Hello from Choiril Kurniawan!")
