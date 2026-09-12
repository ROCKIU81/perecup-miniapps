# Система автоматизации для перекупов автомобилей

Telegram-бот с каталогом автомобилей и Mini App админка для перекупов.

## Структура проекта

```
Перекуп_miniapps/
├── backend/          # Python бэкенд (FastAPI + Telegram Bot)
│   ├── main.py       # API сервер
│   ├── bot.py        # Telegram бот
│   ├── database.py   # Настройка БД
│   ├── models.py     # Модели данных
│   ├── requirements.txt
│   └── .env.example
└── frontend/         # React Mini App
    ├── src/
    │   ├── App.jsx
    │   └── App.css
    ├── package.json
    └── .env
```

## Установка и запуск

### 1. Установка зависимостей

**Бэкенд:**
```bash
cd backend
pip install -r requirements.txt
```

**Фронтенд:**
```bash
cd frontend
npm install
```

### 2. Настройка переменных окружения

**Бэкенд (backend/.env):**
```
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=sqlite:///./cars.db
WEBAPP_URL=https://your-app.railway.app
```

**Фронтенд (frontend/.env):**
```
VITE_API_URL=http://localhost:8000
```

### 3. Получение Telegram Bot Token

1. Найди @BotFather в Telegram
2. Отправь /newbot и следуй инструкциям
3. Скопируй полученный токен в .env файл

### 4. Запуск

**Запуск API сервера:**
```bash
cd backend
python main.py
```

**Запуск Telegram бота:**
```bash
cd backend
python start_bot.py
```

**Запуск Mini App (для разработки):**
```bash
cd frontend
npm run dev
```

## Функционал

### Telegram бот для клиентов:
- 🚗 Каталог всех актуальных автомобилей
- 📋 Карточка лота с фото, ценой, описанием
- 📞 Кнопка "Оставить заявку"
- ❓ Автоответы на частые вопросы
- 🔍 Ответы по описанию конкретного лота

### Mini App админка:
- ➕ Добавление/редактирование/удаление лотов
- 📊 Просмотр заявок от клиентов
- ❓ Управление FAQ
- 📤 Кнопка "Опубликовать" (для будущего автопостинга)

## Настройка Telegram Mini App

### 1. Получение токена бота

1. Найди @BotFather в Telegram
2. Отправь /newbot и следуй инструкциям
3. Скопируй полученный токен в backend/.env

### 2. Создание Mini App через BotFather

1. Найди @BotFather в Telegram
2. Отправь /newapp
3. Выбери своего бота
4. Введи название Mini App (например: "Админ-панель")
5. Введи описание
6. Введи URL твоего фронтенда:
   - Для локальной разработки: `http://localhost:5174`
   - Для продакшена: твой публичный URL (например, Railway)
7. BotFather даст тебе WebApp URL

### 3. Настройка бота для Mini App

В backend/bot.py замени `8993048680` на твой реальный Telegram ID:

```python
is_admin = message.from_user.id == ТВОЙ_TELEGRAM_ID
```

Чтобы узнать свой Telegram ID:
1. Найди @userinfobot в Telegram
2. Отправь любое сообщение
3. Бот покажет твой ID

### 4. Добавление кнопки в бота

После настройки Mini App, кнопка "⚙️ Админ-панель" будет автоматически появляться в боте для админа.

## Развертывание на Railway

### 1. Подготовка репозитория

Залей проект на GitHub.

### 2. Создание проекта на Railway

1. Зарегистрируйся на railway.app
2. Создай новый проект из GitHub
3. Добавь переменные окружения:
   - `BOT_TOKEN` (твой токен бота)
   - `DATABASE_URL` (Railway предоставит PostgreSQL URL)
   - `WEBAPP_URL` (URL твоего приложения)

### 3. Настройка бэкенда

Railway автоматически определит Python и установит зависимости из requirements.txt.

### 4. Настройка фронтенда

1. Создай отдельный проект на Railway для фронтенда
2. Настрой VITE_API_URL на URL бэкенда
3. Railway автоматически соберёт React приложение

### 5. Обновление Mini App URL

После деплоя:
1. Обнови URL в BotFather (/myapps -> edit)
2. Обнови backend/bot.py (измени localhost на Railway URL)
3. Перезапусти бота

## Первичная настройка

1. Запусти бота и API сервер
2. Открой Mini App в Telegram
3. Добавь первый автомобиль через админку
4. Настрой FAQ для автоответов
5. Проверь работу бота через /start

## Следующие этапы

- **Этап 2:** Автопостинг в Telegram канал
- **Этап 3:** Интеграция с Instagram
- **Этап 4:** Аналитика и статистика
- **Этап 5:** Многопользовательность (SaaS)

## Поддержка

Если возникнут проблемы:
1. Проверь логи бэкенда и бота
2. Убедись, что BOT_TOKEN правильный
3. Проверь подключение к базе данных
4. Проверь CORS настройки в main.py
