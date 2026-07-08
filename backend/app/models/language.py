from sqlalchemy import BigInteger, Column, Integer, String

from app.database import Base


class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, nullable=False)
    language = Column(String(100), nullable=False)
    bytes = Column(BigInteger, default=0)
