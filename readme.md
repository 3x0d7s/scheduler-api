# Scheduler API

FastAPI-based REST API for managing schedules and events.

## Project Overview

This project represents an API for creating and managing schedules, events, and subscriptions. The system supports user authentication and various access levels.

## Key Features

- User authentication (JWT)
- Schedule management (public/private)
- Event management within schedules
- Subscription system for schedules
- User roles (regular users/superusers)

## Project Structure

src/
-  auth/ # Authentication
-  events/ # Event management
-  schedules/ # Schedule management
-  subscriptions/ # Subscription system
-  users/ # User management


## Tech Stack

- FastAPI
- SQLAlchemy (async)
- FastAPI Users
- PostgreSQL
- Pydantic

## Data Models

### User
- Base user model with extended fields (name, surname)
- Support for roles (regular user/superuser)

### Schedule
- Name and description of the schedule
- Type of schedule (public/private)
- Association with the owner

### Event
- Name and description of the event
- Day of the week and time of occurrence
- Association with the schedule

### Subscription
- Relationship between user and schedule
- Type of subscription (owner/follower)

## API Endpoints

### Users
- `/auth/jwt/login` - authentication
- `/auth/register` - registration
- `/users/` - user management
- `/me/` - endpoints for authorized users

### Schedules
- CRUD operations for schedules
- Managing subscriptions to schedules
- Filtering by type (public/private)

### Events
- CRUD operations for events in schedules
- Association with specific schedules

## Project Setup

1. Create a `.env` file with the following variables:

- DB_HOST=
- DB_PASSWORD=
- DB_USER=
- DB_NAME=
- DB_PORT=
- SECRET_KEY=

2. Install dependencies
3. Run migrations
4. Start the server