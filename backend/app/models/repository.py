from sqlalchemy import TIMESTAMP, BigInteger, Boolean, Column, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    github_repo_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    primary_language = Column(String(100))
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    is_fork = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP)
    pushed_at = Column(TIMESTAMP)
    synced_at = Column(TIMESTAMP, server_default=func.now())
