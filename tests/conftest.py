import pytest
from app.db.database import db

@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    # Mock database responses
    def mock_execute_single(*args, **kwargs):
        return {"max_id": 0, "test": 1}

    def mock_execute_many(*args, **kwargs):
        return []

    def mock_execute_write(*args, **kwargs):
        return 1

    monkeypatch.setattr(db, "execute_single", mock_execute_single)
    monkeypatch.setattr(db, "execute_many", mock_execute_many)
    monkeypatch.setattr(db, "execute_write", mock_execute_write) 