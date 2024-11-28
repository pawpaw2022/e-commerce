from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # Set to False in production
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Database:
    def __init__(self):
        self.config = {
            'host': settings.MYSQL_HOST,
            'user': settings.MYSQL_USER,
            'password': settings.MYSQL_PASSWORD,
            'database': settings.MYSQL_DB,
            'port': int(settings.MYSQL_PORT),
            'charset': 'utf8mb4'
        }

    @contextmanager
    def get_db(self):
        conn = mysql.connector.connect(**self.config)
        try:
            cursor = conn.cursor(dictionary=True)
            yield cursor
            conn.commit()
        except Error as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def execute_single(self, query, params=None):
        with self.get_db() as cursor:
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return dict(result) if result else None

    def execute_many(self, query, params=None):
        with self.get_db() as cursor:
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            return [dict(row) for row in results]

    def execute_write(self, query, params=None):
        """Execute INSERT, UPDATE, DELETE queries and return last inserted id for INSERTs"""
        with self.get_db() as cursor:
            cursor.execute(query, params or ())
            if query.strip().upper().startswith('INSERT'):
                return cursor.lastrowid
            return cursor.rowcount

# Create a single instance to be used throughout the application
db = Database()

# Make sure to export the db instance
__all__ = ['db'] 