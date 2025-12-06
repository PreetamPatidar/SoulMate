# SoulMate

A real-time chat application built with Django, Django Channels, and vanilla JavaScript.

## Overview

SoulMate is a modern chat application that allows users to communicate in real-time through text messages. It features user authentication, chat rooms (one-on-one and group chats), real-time messaging via WebSockets, and a responsive web interface.

## Features

- **User Authentication**: Register and login functionality with JWT tokens
- **Real-time Messaging**: Instant message delivery using WebSockets
- **Chat Rooms**: Support for one-on-one and group conversations
- **Message History**: Paginated message loading with scrolling support
- **Online Status**: User online/offline status tracking
- **Typing Indicators**: Real-time typing status updates
- **Read Receipts**: Message read status tracking
- **Responsive Design**: Mobile-friendly web interface

## Technology Stack

### Backend
- **Django**: Web framework for building the API
- **Django REST Framework**: For building RESTful APIs
- **Django Channels**: For WebSocket support and real-time features
- **PostgreSQL**: Database for data persistence
- **Redis**: For channel layers in Django Channels

### Frontend
- **HTML5**: Structure and markup
- **CSS3**: Styling and responsive design
- **Vanilla JavaScript**: Client-side logic and API interactions

## Project Structure

```
SoulMate-1/
├── backend/                    # Django backend application
│   ├── soulmate/              # Main Django project
│   │   ├── __init__.py
│   │   ├── asgi.py            # ASGI configuration for WebSockets
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py            # URL routing
│   │   └── wsgi.py
│   ├── chat/                  # Chat application
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── consumers.py       # WebSocket consumers
│   │   ├── models.py          # Database models
│   │   ├── routing.py         # WebSocket routing
│   │   ├── serializers.py     # API serializers
│   │   └── views.py           # API views
│   ├── manage.py              # Django management script
│   └── requirements.txt       # Python dependencies
├── web/                       # Frontend application
│   ├── index.html             # Main HTML file
│   └── static/                # Static assets
│       ├── css/
│       │   └── style.css      # CSS styles
│       └── js/
│           └── auth.js        # Authentication JavaScript
├── LICENSE
├── README.md                  # This file
└── TODO.md                    # Project tasks and progress
```

## Backend Implementation

### Models
- **User**: Custom user model with email authentication, profile picture, and online status
- **ChatRoom**: Supports one-on-one and group chats with participant management
- **Message**: Handles text, image, and file messages with read receipts

### API Endpoints
- `POST /api/auth/register/`: User registration
- `POST /api/auth/login/`: User login with JWT tokens
- `GET /api/chats/`: List user's chat rooms
- `POST /api/chats/`: Create new chat room
- `GET /api/chats/{id}/messages/`: Get messages for a chat room
- `GET /api/users/search/`: Search users
- `GET/PUT /api/users/profile/`: Get/update user profile

### WebSocket Implementation
- Real-time message sending and receiving
- Typing indicators
- Read receipts
- Connection management with authentication

## Frontend Implementation

### Authentication
- Login/Register forms with tab switching
- JWT token management and storage
- Automatic token verification on page load

### Chat Interface
- Sidebar with chat room list
- Main chat area with message display
- Message input with send functionality
- Real-time message updates
- Responsive design for mobile devices

### Real-time Features
- WebSocket connection management
- Live message delivery
- Typing status updates
- Message read status

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis
- Node.js (for serving frontend, optional)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SoulMate-1
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure database**
   - Create PostgreSQL database
   - Update `settings.py` with your database credentials

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start Redis server**
   ```bash
   # Install and start Redis
   redis-server
   ```

7. **Run the server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Serve the frontend**
   - Open `web/index.html` in a web browser
   - Or use a simple HTTP server:
   ```bash
   cd web
   python -m http.server 8080
   ```

2. **Access the application**
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:8080 or open `web/index.html` directly

## Usage

1. **Register**: Create a new account with email and password
2. **Login**: Sign in with your credentials
3. **Create Chat**: Click "New Chat" to start a conversation
4. **Send Messages**: Type and send messages in real-time
5. **Switch Chats**: Click on different chat rooms in the sidebar

## Development Status

### Completed Features
- ✅ User authentication (register/login)
- ✅ Chat room creation and management
- ✅ Real-time messaging via WebSockets
- ✅ Message history with pagination
- ✅ User search functionality
- ✅ Profile management
- ✅ Responsive web interface
- ✅ Typing indicators
- ✅ Read receipts
- ✅ Online status tracking

### In Progress / Planned
- 🔄 File/image sharing in messages
- 🔄 Push notifications
- 🔄 Message reactions and replies
- 🔄 Voice/video calling
- 🔄 Message encryption
- 🔄 Mobile app development

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Django and Django Channels
- Real-time functionality powered by WebSockets
- Responsive design with modern CSS
- Inspired by modern chat applications
# soulmate
