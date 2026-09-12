# Быстрый деплой на Railway (HTTPS URL за 5-10 минут)

## План деплоя

Создадим **2 отдельных проекта** на Railway:
1. **Backend** — API сервер + база данных
2. **Frontend** — Mini App для Telegram

## Шаг 1: Подготовка репозитория

```bash
git init
git add .
git commit -m "Initial commit"
```

Залей на GitHub и создай репозиторий.

## Шаг 2: Деплой Backend на Railway

1. Зайди на [railway.app](https://railway.app)
2. Нажми "New Project" → "Deploy from GitHub repo"
3. Выбери свой репозиторий
4. Railway автоматически определит Python и установит зависимости

**Настройка переменных окружения:**
- `BOT_TOKEN` = `8993048680:AAGdUClcVN9At-yi1D-Buj0Wi5s5hk1yGFg`
- `DATABASE_URL` = Railway предоставит автоматически (PostgreSQL)
- `WEBAPP_URL` = URL фронтенда (получим на шаге 3)

**Файл для backend:**
Создай `backend/Procfile`:
```
web: python main.py
```

## Шаг 3: Деплой Frontend на Railway

1. Создай ещё один проект на Railway
2. Выбери тот же GitHub репозиторий
3. В настройках укажи "Root directory" = `frontend`
4. Railway автоматически соберёт React

**Настройка переменных окружения:**
- `VITE_API_URL` = URL бэкенда из шага 2

## Шаг 4: Получение HTTPS URL

После деплоя Railway покажет:
- Backend URL: `https://xxxxx.up.railway.app`
- Frontend URL: `https://xxxxx.up.railway.app`

## Шаг 5: Настройка Telegram Mini App

1. @BotFather → /newapp
2. Выбери своего бота
3. URL: `https://xxxxx.up.railway.app` (Frontend URL)
4. Получи WebApp URL

## Шаг 6: Обновление конфигурации

Обнови `backend/.env`:
```
WEBAPP_URL=https://xxxxx.up.railway.app
```

Обнови `backend/bot.py`:
```python
is_admin = message.from_user.id == 8496050088
```

## Альтернатива: Один проект с двумя сервисами

Если хочешь один проект, создай `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "builds": [
    {
      "name": "backend",
      "dockerContext": "./backend",
      "dockerfile": "Dockerfile"
    },
    {
      "name": "frontend", 
      "dockerContext": "./frontend",
      "dockerfile": "Dockerfile"
    }
  ]
}
```

## Преимущества Railway

✅ Бесплатный тариф ($5 кредитов/месяц)
✅ Автоматический HTTPS
✅ Автоматический деплой из GitHub
✅ PostgreSQL бесплатно
✅ Простая настройка

## Время деплоя

- Backend: ~3-5 минут
- Frontend: ~2-3 минуты
- Настройка Mini App: ~2 минуты

**Итого: ~10 минут до рабочей системы с HTTPS!**
