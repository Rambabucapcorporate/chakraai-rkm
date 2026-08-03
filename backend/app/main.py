from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.core.config import settings

# Import all models so SQLAlchemy registers them before creating tables
from app.models.user import User  # noqa: F401

# Create all database tables (Disabled as we use existing table)
# Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="RKM Academic Assistant API",
    description="Backend API for Ramakrishna Mission Vivekananda College's Academic Assistant",
    version="2.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chakra.rkmvc.ac.in"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================== ROOT REDIRECT ==================
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# ================== REGISTER ROUTERS ==================
from app.api.routers.auth import router as auth_router
from app.api.routers.chat import router as chat_router
from app.api.routers.admin import router as admin_router

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(admin_router)


# ================== RUN SERVER ==================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
