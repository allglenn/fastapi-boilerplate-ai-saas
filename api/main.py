from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from views import user as user_views
from views import auth as auth_views
from db.database import init_db
import asyncio

app = FastAPI(title="Api ", version="1.0.0", description="boilerplate api project")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

# Add health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Include routers
app.include_router(auth_views.router, prefix="/api/v1")
app.include_router(user_views.router, prefix="/api/v1") 