import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import uuid

from app.main import app
from app.database import Base, get_db
from app.models import CategoryEnum, PriorityEnum, StatusEnum, Complaint
from app.redis_client import redis_client

# SQLITE for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    # Setup fresh tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    # Very simple mock for redis
    mock_store = {}
    
    def mock_get(key):
        return mock_store.get(key)
    
    def mock_setex(key, ttl, value):
        mock_store[key] = value
        
    def mock_delete(key):
        if key in mock_store:
            del mock_store[key]
            
    class MockPipeline:
        def __init__(self):
            self.cmds = []
        def incr(self, key):
            self.cmds.append(("incr", key))
        def ttl(self, key):
            self.cmds.append(("ttl", key))
        def execute(self):
            res = []
            for cmd, key in self.cmds:
                if cmd == "incr":
                    mock_store[key] = mock_store.get(key, 0) + 1
                    res.append(mock_store[key])
                elif cmd == "ttl":
                    res.append(60)
            return res
            
    monkeypatch.setattr(redis_client, "get", mock_get)
    monkeypatch.setattr(redis_client, "setex", mock_setex)
    monkeypatch.setattr(redis_client, "delete", mock_delete)
    monkeypatch.setattr(redis_client, "pipeline", MockPipeline)
    monkeypatch.setattr(redis_client, "expire", lambda k, t: None)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_complaint(setup_db):
    db = TestingSessionLocal()
    complaint = Complaint(
        id=uuid.uuid4(),
        text="A sample complaint",
        location="Sector 1",
        category=CategoryEnum.other,
        priority=PriorityEnum.normal,
        status=StatusEnum.open
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    db.close()
    return complaint
