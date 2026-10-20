from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from uuid import UUID 
from typing import Optional, Literal



class BaseResponse(BaseModel):
    task_id: UUID  # Переименовал в task_id для ясности, как в ТЗ



class PredictionRequest(BaseModel):
    
    text: str = Field(..., min_length=5, max_length=2000, description="Текст отзыва")

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        v = v.strip() # Сначала чистим
        if not v:
            raise ValueError("Текст не может состоять только из пробелов")
        return v



class PredictionResponse(BaseResponse): # Наследуем task_id отсюда
    status: Literal["pending", "processing", "done", "failed"]
    cached: bool



class TaskResponse(BaseModel):
    task_id: UUID
    status: Literal["pending", "processing", "done", "failed"]
    sentiment: Optional[Literal["positive", "neutral", "negative"]] = None
    confidence: Optional[float] = None
    is_toxic: Optional[bool] = None
    created_at: datetime # Pydantic сам сконвертирует это в строку при ответе
    completed_at: Optional[datetime] = None



class PredictionResult(BaseModel):
    sentiment: Literal["positive", "neutral", "negative"]
    confidence: float
    is_toxic: bool
    created_at: datetime