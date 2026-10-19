from app.models.base import Base 
from sqlalchemy.orm import Mapped, mapped_column


class Reviews(Base):

    text : Mapped[str] 
    status : Mapped[str] = mapped_column(default = "pending")
    sentiment : Mapped[str] = mapped_column(nullable = True)
       