from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from sqlalchemy.orm import Session

import os

engine = create_engine(
    "postgresql",
    username=os.environ.get('POSTGRES_USER', ''),
    password=os.environ.get('POSTGRES_PASSWORD', ''),
    host=os.environ.get('POSTGRES_HOSTNAME', ''),
    port=os.environ.get('POSTGRES_PORT', ''),
    database=os.environ.get('POSTGRES_DB', ''),
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Subscriber(Base):
    __tablename__ = "subscribers"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, index=True)

def subscribe(chat_id: int, db: Session):
    existing_user = db.query(Subscriber).filter(Subscriber.chat_id == chat_id).first()
    if not existing_user:
        new_subscriber = Subscriber(chat_id=chat_id)
        db.add(new_subscriber)
        db.commit()
        return {"message": "Subscribed successfully"}
    else:
        raise HTTPException(status_code=404, detail="Subscriber not found")

def unsubscribe(chat_id: int, db: Session):
    subscriber_to_remove = db.query(Subscriber).filter(Subscriber.chat_id == chat_id).first()
    if subscriber_to_remove:
        db.delete(subscriber_to_remove)
        db.commit()
        return {"message": "Unsubscribed successfully"}
    else:
        raise HTTPException(status_code=404, detail="Subscriber not found")

Base.metadata.create_all(bind=engine)
