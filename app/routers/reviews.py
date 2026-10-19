from fastapi import APIRouter, status, Depends
from app.schemas.review import ReviewCreate, ReviewCreateResponse, ReviewStatus
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db


reviews_routers = APIRouter(prefix = "/api/v1/reviews", tags = ["reviews"])


@reviews_routers.post("", status_code = status.HTTP_201_CREATED)
async def create_review(review : ReviewCreate, db : AsyncSession = Depends(get_db)):
    
    try:
        review_create = ...

        db.add(review_create)

        db.commit()

        await ReviewCreateResponse(id = review.id, status = ReviewStatus.PENDING)
    except:
        db.rollback()
