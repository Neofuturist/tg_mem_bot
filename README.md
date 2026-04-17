# Telegram Memory Training Bot

A simple Telegram bot for memory sequence training built with `python-telegram-bot` (asyncio, v21+).

## Features

- Random letter sequence generation
- Two alphabets: English and Russian
- Settings:
  - Alphabet (`en` / `ru`)
  - Length mode:
    - fixed length
    - range `min-max`
  - Repeats (`on` by default, can be toggled `on/off`)
- Training flow:
  1. Generate sequence
  2. Show sequence
  3. Press **"Запомнил"**
  4. Bot hides/deletes shown sequence
  5. User enters answer
  6. Bot checks answer (case-insensitive)
  7. Bot returns correct/incorrect and shows original with highlighted errors (bold)
- In-memory per-user state storage keyed by user id
- Command-based control: `/help`, `/setup`, `/play`
- `/start` resets session data and opens inline main menu
- Persistent reply-keyboard buttons under the input field are removed

## Project structure

- `main.py` — entrypoint
- `config.py` — BOT_TOKEN loading
- `handlers/`
  - `messages.py` — `/start`, text input handling
  - `callbacks.py` — inline button callbacks
- `services/`
  - `sequence_service.py` — sequence generation
  - `check_service.py` — answer checking and error highlighting
- `models/`
  - `user_state.py` — enums/dataclasses for user state
- `storage/`
  - `user_state_repository.py` — in-memory user state repository
- `keyboards/`
  - `inline.py` — inline keyboards
- `requirements.txt`

## Run

1. Use Python 3.14 (recommended) and install dependencies:

```bash
python3.14 -m pip install --upgrade pip
python3.14 -m pip install -r requirements.txt
```

2. Create `.env` from example and set token:

```bash
cp .env.example .env
```

Then open `.env` and set:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

`BOT_TOKEN` from environment variables is still supported (for example, via `export BOT_TOKEN=...`).

3. Start bot:

```bash
python main.py
```

## Deployment

### Docker

Build image:

```bash
docker build -t memory-bot .
```

Run container with env file:

```bash
docker run -d --name memory-bot --env-file .env memory-bot
```

### systemd (Linux server)

1. Edit `memory-bot.service` and set correct paths/user:
   - `WorkingDirectory=/opt/memory-bot`
   - `EnvironmentFile=/opt/memory-bot/.env`
   - `ExecStart=/opt/memory-bot/.venv/bin/python /opt/memory-bot/main.py`

2. Install service unit:

```bash
sudo cp memory-bot.service /etc/systemd/system/memory-bot.service
sudo systemctl daemon-reload
```

3. Enable and start:

```bash
sudo systemctl enable memory-bot
sudo systemctl start memory-bot
sudo systemctl status memory-bot
```

## Compatibility notes

- Runtime dependencies are pure-Python-friendly for Python 3.14 environments.
- Removed aiogram/aiohttp/pydantic-core dependency chain from this project to avoid wheel build failures.
- Storage is in-memory only (data is lost on process restart).
- Bot texts are in Russian for user-facing clarity.
