from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import declarative_base

class Settings(BaseSettings):
    """
    Configurações gerais uadas na aplicação
    """

    API_V1_STR : str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://william:1234@localhost:5432/faculdade"
    DBBaseModel = declarative_base()

    # Código Legado
    #class Cnfig:
    #    case_sensitive = True

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()