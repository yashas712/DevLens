from sqlalchemy import TIMESTAMP, Column, Integer, String, Text

from app.database import Base


class Commit(Base):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, nullable=False)
    sha = Column(String(40), nullable=False)
    author_name = Column(String(255))
    author_email = Column(String(255))
    message = Column(Text)
    additions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    committed_at = Column(TIMESTAMP, nullable=False)
