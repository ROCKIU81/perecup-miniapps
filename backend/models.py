from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    mileage = Column(Integer, nullable=False)
    condition = Column(String, default="Не бита/не крашена")
    photo_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    requests = relationship("Request", back_populates="car")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    requests = relationship("Request", back_populates="user")

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    car = relationship("Car", back_populates="requests")
    user = relationship("User", back_populates="requests")

class FAQ(Base):
    __tablename__ = "faq"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False, unique=True)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
