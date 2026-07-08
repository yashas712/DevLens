from sqlalchemy import TIMESTAMP, Column, Integer, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.database import Base


class DeveloperScore(Base):
    __tablename__ = "developer_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    score = Column(Numeric(6, 2), nullable=False)
    breakdown_json = Column(JSONB)
    computed_at = Column(TIMESTAMP, server_default=func.now())
