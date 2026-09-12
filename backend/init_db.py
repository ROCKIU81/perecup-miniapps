from database import engine, Base, SessionLocal
from models import Car, FAQ

def init_database():
    # Создаём таблицы
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Добавляем тестовые FAQ
    if not db.query(FAQ).first():
        faqs = [
            FAQ(
                question="где находитесь",
                answer="Мы находимся в Москве. Вы можете посмотреть автомобиль по адресу: ул. Примерная, д. 1"
            ),
            FAQ(
                question="какой договор",
                answer="Мы работаем по договору купли-продажи, оформленному согласно законодательству РФ. Все документы в порядке."
            ),
            FAQ(
                question="доставка",
                answer="Доставка возможна по всей России. Стоимость рассчитывается индивидуально в зависимости от расстояния."
            ),
            FAQ(
                question="торг",
                answer="Небольшой торг возможен при осмотре автомобиля."
            ),
            FAQ(
                question="кредит",
                answer="Помогаем с оформлением кредита. Работаем с несколькими банками."
            )
        ]
        
        for faq in faqs:
            db.add(faq)
        
        db.commit()
        print("Добавлены тестовые FAQ")
    
    # Добавляем тестовый автомобиль
    if not db.query(Car).first():
        test_car = Car(
            title="Toyota Camry 2020",
            description="Отличное состояние, один владелец, обслуживался у официального дилера. Полная история обслуживания. Не бита, не крашена. Все опции работают.",
            price=1850000,
            year=2020,
            mileage=45000,
            condition="Не бита/не крашена",
            photo_url="https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800",
            is_active=True,
            is_published=False
        )
        
        db.add(test_car)
        db.commit()
        print("Добавлен тестовый автомобиль")
    
    db.close()
    print("База данных инициализирована!")

if __name__ == "__main__":
    init_database()
