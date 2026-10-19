from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 
from uuid import uuid4 

class Base(DeclarativeBase):

    id : Mapped[str] = mapped_column(primary_key = True, default = lambda : str(uuid4()))