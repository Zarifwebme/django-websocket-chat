# Django Live Chat (WebSocket)

Real-time chat application built with Django Channels and WebSocket.

## Features

- WebSocket real-time messaging
- Chat rooms
- Online users indicator
- Typing indicator
- Message history
- Modern UI

## Tech Stack

- Django
- Django Channels
- WebSocket
- SQLite
- HTML / CSS / JS

## Run locally

```bash
git clone https://github.com/yourname/django-live-chat.git
cd django-live-chat

python -m venv .venv
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver