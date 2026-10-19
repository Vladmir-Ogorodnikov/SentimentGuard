from dataclasses import dataclass 
import os
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:

    database_url : str 


def get_settings() -> Settings:

    return Settings(os.getenv("DATABASE_URL")

    )