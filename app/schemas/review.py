from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from uuid import UUID 
from typing import Optional
from dataclasses import dataclass

@dataclass
class ReviewStatus:
      PENDING = "pending"
      PROCESSING = "processing"
      DONE = "done"
      FAILED = "failed"



class Base(BaseModel):

      id : UUID

class ReviewCreate(Base):

      model_config = ConfigDict(from_attributes = True) #позволяет создать схему из sqlalchemy объекта

      text : str 
      

      @field_validator("text")
      def validate_text(v : str):

            if len(v) < 5 or len(v) > 2000:
                  raise ValueError("Недопустимая длинна текста")
            return v.strip()
      
class ReviewResponse(Base):

      text : str
      status : ...
      sentiment : ...
      confidence: Optional[float] = None
      is_toxic : Optional[bool] = None 
      error_message : Optional[str] = None 
      created_at : datetime
      processed_at: Optional[datetime] = None

class ReviewCreateResponse(Base):

      status : ReviewStatus      






