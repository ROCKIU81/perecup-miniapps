from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from datetime import datetime
from dotenv import load_dotenv

from database import engine, get_db, Base
from models import Car, User, Request, FAQ
from pydantic import BaseModel, ConfigDict

load_dotenv()

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Reseller API")

# CORS для Mini App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic модели
class CarBase(BaseModel):
    title: str
    description: str
    price: int
    year: int
    mileage: int
    condition: str = "Не бита/не крашена"
    photo_url: str = None

class CarCreate(CarBase):
    pass

class CarResponse(CarBase):
    id: int
    is_active: bool
    is_published: bool
    created_at: str

    model_config = ConfigDict(from_attributes=True)

class RequestBase(BaseModel):
    car_id: int
    message: str

class RequestCreate(RequestBase):
    telegram_id: int

class RequestResponse(RequestBase):
    id: int
    is_processed: bool
    created_at: str

    model_config = ConfigDict(from_attributes=True)

class FAQBase(BaseModel):
    question: str
    answer: str

class FAQCreate(FAQBase):
    pass

class FAQResponse(FAQBase):
    id: int
    created_at: str

    model_config = ConfigDict(from_attributes=True)

# API endpoints
@app.get("/api/cars", response_model=List[CarResponse])
def get_cars(db: Session = Depends(get_db)):
    cars = db.query(Car).filter(Car.is_active == True).all()
    # Конвертируем datetime в string
    result = []
    for car in cars:
        car_dict = {
            "id": car.id,
            "title": car.title,
            "description": car.description,
            "price": car.price,
            "year": car.year,
            "mileage": car.mileage,
            "condition": car.condition,
            "photo_url": car.photo_url,
            "is_active": car.is_active,
            "is_published": car.is_published,
            "created_at": car.created_at.isoformat() if car.created_at else ""
        }
        result.append(car_dict)
    return result

@app.get("/api/cars/{car_id}", response_model=CarResponse)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return {
        "id": car.id,
        "title": car.title,
        "description": car.description,
        "price": car.price,
        "year": car.year,
        "mileage": car.mileage,
        "condition": car.condition,
        "photo_url": car.photo_url,
        "is_active": car.is_active,
        "is_published": car.is_published,
        "created_at": car.created_at.isoformat() if car.created_at else ""
    }

@app.post("/api/cars", response_model=CarResponse)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    db_car = Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

@app.put("/api/cars/{car_id}", response_model=CarResponse)
def update_car(car_id: int, car: CarCreate, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    for key, value in car.dict().items():
        setattr(db_car, key, value)
    
    db.commit()
    db.refresh(db_car)
    return db_car

@app.delete("/api/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    db_car.is_active = False
    db.commit()
    return {"message": "Car deleted"}

@app.post("/api/cars/{car_id}/publish")
def publish_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    db_car.is_published = True
    db.commit()
    return {"message": "Car published"}

@app.get("/api/requests", response_model=List[RequestResponse])
def get_requests(db: Session = Depends(get_db)):
    requests = db.query(Request).all()
    result = []
    for req in requests:
        req_dict = {
            "id": req.id,
            "car_id": req.car_id,
            "user_id": req.user_id,
            "message": req.message,
            "is_processed": req.is_processed,
            "created_at": req.created_at.isoformat() if req.created_at else ""
        }
        result.append(req_dict)
    return result

@app.post("/api/requests", response_model=RequestResponse)
def create_request(request: RequestCreate, db: Session = Depends(get_db)):
    # Находим или создаем пользователя
    user = db.query(User).filter(User.telegram_id == request.telegram_id).first()
    if not user:
        user = User(telegram_id=request.telegram_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    db_request = Request(
        car_id=request.car_id,
        user_id=user.id,
        message=request.message
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return {
        "id": db_request.id,
        "car_id": db_request.car_id,
        "user_id": db_request.user_id,
        "message": db_request.message,
        "is_processed": db_request.is_processed,
        "created_at": db_request.created_at.isoformat() if db_request.created_at else ""
    }

@app.put("/api/requests/{request_id}/process")
def process_request(request_id: int, db: Session = Depends(get_db)):
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    db_request.is_processed = True
    db.commit()
    return {"message": "Request processed"}

@app.get("/api/faq", response_model=List[FAQResponse])
def get_faq(db: Session = Depends(get_db)):
    faq = db.query(FAQ).all()
    result = []
    for item in faq:
        item_dict = {
            "id": item.id,
            "question": item.question,
            "answer": item.answer,
            "created_at": item.created_at.isoformat() if item.created_at else ""
        }
        result.append(item_dict)
    return result

@app.post("/api/faq", response_model=FAQResponse)
def create_faq(faq: FAQCreate, db: Session = Depends(get_db)):
    db_faq = FAQ(**faq.dict())
    db.add(db_faq)
    db.commit()
    db.refresh(db_faq)
    return {
        "id": db_faq.id,
        "question": db_faq.question,
        "answer": db_faq.answer,
        "created_at": db_faq.created_at.isoformat() if db_faq.created_at else ""
    }

@app.delete("/api/faq/{faq_id}")
def delete_faq(faq_id: int, db: Session = Depends(get_db)):
    db_faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not db_faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    
    db.delete(db_faq)
    db.commit()
    return {"message": "FAQ deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
