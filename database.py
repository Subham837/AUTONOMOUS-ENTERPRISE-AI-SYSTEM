from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Use check_same_thread=False for SQLite + FastAPI compatibility
engine = create_engine("sqlite:///enterprise.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)

Base.metadata.create_all(bind=engine)