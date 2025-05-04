from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GlobalGuessCount(Base):
    __tablename__ = "guess_counts"
    guess = Column(String, primary_key=True)
    count = Column(Integer, default=1)
