from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.config import auth_backend, fastapi_users
from src.events.routers import router as events_router
from src.schedules.routers import router as schedules_router
from src.subscriptions.routers import router as subscriptions_router
from src.users.routers import router as user_routers
from src.users.routers_protected import router as user_routers_protected
from src.users.schemas import UserRead, UserCreate

app = FastAPI(
    title="Scheduler API"
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(schedules_router)
app.include_router(events_router)
app.include_router(subscriptions_router)
app.include_router(user_routers)
app.include_router(user_routers_protected)

current_user = fastapi_users.current_user()
