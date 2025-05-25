from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from contextlib import asynccontextmanager
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routes import message, session
from app.utils.logger import setup_logger
from app.database.utils import init_db
import logging

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chat Storage Microservice",
    description="API for storing and managing RAG-based chat sessions",
    version="1.0.0"
)

# Setup logger
setup_logger()
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(message.router, prefix="/chat", tags=["Chat"])
app.include_router(session.router, prefix="/chat", tags=["Session"])


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application")
    await init_db()
    yield
    logger.info("Shutting down application")
