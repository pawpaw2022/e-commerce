from sqlalchemy_utils import database_exists, create_database
from .database import engine, Base
from .config import settings

def init_db():
    try:
        # Create database if it doesn't exist
        if not database_exists(engine.url):
            create_database(engine.url)
            print(f"Created database: {settings.MYSQL_DB}")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Created all tables successfully")
        
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_db() 