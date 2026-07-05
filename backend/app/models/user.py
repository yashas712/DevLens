from sqlalchemy import Column, Integer, BigInteger, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(255), nullable=False)
    avatar_url = Column(Text)
    access_token = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    last_synced_at = Column(TIMESTAMP)
