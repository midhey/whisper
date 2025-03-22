# 🧠 Whisper Transcriber Bot

Проект для автоматической транскрипции аудиофайлов с помощью OpenAI Whisper API. Поддерживает форматы `.mp3`, `.wav`, `.ogg` (Telegram) и другие. Обрабатывает файлы из папки `audio/`, логирует результат в `logs/`, и сохраняет текстовую расшифровку в `output.txt`.

---

## 🚀 Возможности

- Поддержка аудиоформатов: `.mp3`, `.mp4`, `.mpeg`, `.mpga`, `.m4a`, `.wav`, `.webm`, `.ogg`
- Конвертация `.ogg` → `.wav` через `ffmpeg` (нужно для Telegram)
- Поддержка Docker и Docker Compose
- Логирование успешных и неуспешных транскрипций (`output.log`, `error.log`)
- Структура с разделением кода: `logger.py`, `transcribe.py`

---

## 🧱 Структура проекта

```
├── audio/             # Папка для аудиофайлов
├── logs/              # Папка для логов
├── output.txt         # Файл с результатами транскрипции
├── transcribe.py      # Основной скрипт
├── logger.py          # Логирование
├── Dockerfile         # Образ Docker
├── docker-compose.yml # Сборка и запуск
├── .env               # Переменные окружения (API-ключ)
└── requirements.txt   # Python-зависимости
```

---

## 🛠️ Установка

### 1. Создай `.env` файл

```env
OPENAI_API_KEY=sk-ваш-ключ
```

### 2. Помести аудиофайлы в папку `audio/`

Файлы `.ogg` (например, из Telegram) тоже можно — они будут автоматически сконвертированы.

### 3. Собери и запусти через Docker

```bash
docker-compose up --build
```

После завершения скрипта:

- результаты будут в `output.txt`
- логи в `logs/output.log` и `logs/error.log`

---

## 🧰 Зависимости

### `requirements.txt`

```txt
openai==1.68.2
```

### `Dockerfile`

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Установка системных зависимостей, включая ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY transcribe.py transcribe.py
COPY logger.py logger.py

CMD ["python", "transcribe.py"]
```

---

## 🐳 docker-compose.yml

```yaml
version: "3.8"

services:
  transcriber:
    build: .
    env_file:
      - .env
    volumes:
      - ./audio:/app/audio
      - ./logs:/app/logs
      - type: bind
        source: ./output.txt
        target: /app/output.txt
```

---

## 📋 Логи

- `logs/output.log` — успешная информация (DEBUG + INFO)
- `logs/error.log` — ошибки (WARNING + ERROR)
- логирование настраивается через `logger.py`

---

## 🧪 Пример запуска

```bash
# Клонируем/скачиваем проект
# Помещаем аудио в папку ./audio
# Создаём .env с API-ключом
# Запускаем:
docker-compose up --build
```

---

## 📎 Примечания

- Для `.ogg` файлов требуется `ffmpeg` — он уже устанавливается в Dockerfile.
- `output.txt` будет перезаписан при каждом запуске.
- Whisper API работает на английском и многих других языках.

---

## 📜 Лицензия

MIT
