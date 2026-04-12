from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    RAZORPAY_KEY_ID: str
    RAZORPAY_KEY_SECRET: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    DATABASE_URL: str # Add this line!
    

    # This replaces 'class Config'
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()