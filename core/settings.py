from pydantic_settings import BaseSettings
from pydantic import field_validator
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str
    
    # Directory settings
    UPLOAD_DIR:str
    VECTOR_STORE_DIR:str
    MONITORING_DIR:str

    # Hugging Face API
    HUGGINGFACEHUB_API_TOKEN:str
    HF_EMBEDDING_MODEL:str
    
    # Google API
    CHAT_MODEL:str
    MODEL_PROVIDER:str
    GOOGLE_API_KEY:str
    TEMPERATURE:float | int

    # Databse
    MONGO_URL:str
    MONGO_DB_NAME:str
    N_MESSAGES:int

    # Vector Store Query
    VECTOR_STORE_NAME:str
    TOP_K_CONTEXT_RESULTS:int

    # Ports
    APP_PORT: int

    @field_validator("APP_PORT", "TOP_K_CONTEXT_RESULTS", "TEMPERATURE", "N_MESSAGES", mode="before")
    @classmethod
    def validate_app_port(cls, value, info):
        if isinstance(value, str) and info.field_name != "APP_PORT_SERVER":
            try:
                value = float(value)
                if value.is_integer():
                    return int(value)
                return value
            except ValueError:
                raise ValueError(f"Invalid value for {info.field_name}: {value}. Expected a number.")
        else:
            match info.field_name:
                case "APP_PORT": return 8000
                case "TOP_K_CONTEXT_RESULTS": return 5
                case "TEMPERATURE": return 0.3
                case "N_MESSAGES": return 10
                case _: return 0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create an instance of Settings
settings = Settings()
