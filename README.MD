# 🎭 Theater API

## 🛠 Technologies

- Python 3.12
- Django REST Framework
- Docker & Docker Compose
- Git

---

## 🚀 Features

### Actors
- List all actors (`GET /actors/`)
- Retrieve actor details with `full_name` (`GET /actors/{id}/`)
- Admin-only: Create, update, delete actors

### Genres
- List all genres (`GET /genres/`)
- Admin-only: Create, update, delete genres

### Plays
- List all plays (`GET /plays/`) with actors and genres (short description)
- Retrieve play details (`GET /plays/{id}/`) with full actor and genre info
- Admin-only: Create, update, delete plays

### Theater Halls
- List theater halls (`GET /theater_halls/`)
- Admin-only: Create, update, delete halls

### Performances
- List performances (`GET /performances/`) with play and hall info
- Retrieve performance details (`GET /performances/{id}/`) with nested play and hall info
- Admin-only: Create, update, delete performances

### Reservations
- List reservations for current user (`GET /reservations/`)
- Create reservations (`POST /reservations/`) for logged-in users
- Reservations are tied to the authenticated user automatically

### Tickets
- List tickets (`GET /tickets/`) with play title
- Retrieve ticket details (`GET /tickets/{id}/`) with nested performance, play, hall
- Admin and authenticated users have controlled access
- Create tickets (`POST /tickets/`) with validation for seat availability
- Seat validation ensures row/seat limits and prevents double-booking

## 🐳 Docker
```bash
docker-compose build
docker-compose up
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
```

## 🔑 Authentication

Users must be authenticated to create reservations and tickets

Admin permissions required for managing actors, genres, plays, halls, and performances
