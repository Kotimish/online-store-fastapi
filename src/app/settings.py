from enum import Enum
from pathlib import Path

from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class RepositoryType(str, Enum):
    IN_MEMORY = "in_memory"
    JSON = "json"
    XML = "xml"
    DATABASE = "database"


class JsonRepoSettings(BaseModel):
    products_file: Path
    categories_file: Path

    @field_validator("*", mode="before")
    def resolve_path(cls, v):
        return Path(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PC_SHOP__",
        env_nested_delimiter="_",
        env_file=(
            ".env.default",
            ".env",
        ),
    )
    debug: bool = False
    repository_type: RepositoryType = RepositoryType.IN_MEMORY


settings = Settings()
