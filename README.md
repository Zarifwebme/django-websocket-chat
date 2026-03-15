# Django Live Chat (WebSocket)

Real-time chat web app built with Django, Django Channels, and WebSocket.
Pair test update line for collaboration.

## Features

- Real-time messaging with WebSocket
- Multiple chat rooms
- Online users list (per room)
- Typing indicator
- Message history saved to SQLite
- Clean browser UI

## Tech Stack

- Python 3.10+
- Django 5
- Django Channels 4
- Daphne (ASGI server)
- SQLite
- HTML / CSS / JavaScript

## Quick Start

1. Clone the repository

```bash
git clone <your-repo-url>
cd LiveChat
```

2. Create and activate virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Apply migrations

```bash
python manage.py migrate
```

5. Run development server

```bash
python manage.py runserver
```

6. Open in browser

```text
http://127.0.0.1:8000/
```

## How to Use

1. Open the home page.
2. Enter your username and room name.
3. Join chat and start messaging in real time.

Room names are automatically converted to slug format for URL safety.

## WebSocket Endpoint

The app uses this route internally:

```text
ws://127.0.0.1:8000/ws/chat/<room_name>/
```

## Project Structure

```text
config/      Django project settings and ASGI/URL config
livechat/    Chat app (views, models, consumers, routes)
templates/   HTML templates for index and room pages
db.sqlite3   Local development database
```

## Notes

- Channel layer is configured with `InMemoryChannelLayer` (good for development).
- Current online user tracking is in-memory and reset when server restarts.

## License

This project currently has no explicit license file.