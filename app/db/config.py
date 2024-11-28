from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MySQL connection settings
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "lusining123"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    MYSQL_DB: str = "ecommerce"
    
    # Construct Database URL
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

    class Config:
        env_file = ".env"

settings = Settings() 