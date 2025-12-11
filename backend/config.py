from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    API_PORT: int = 8001
    
    # LLM (OpenAI Compatible)
    OPENAI_API_KEY: str = "sk-mock-key"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-3.5-turbo"
    
    # Database
    FALKORDB_HOST: str = "localhost"
    FALKORDB_PORT: int = 6379
    
    # Discord
    DISCORD_TOKEN: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
