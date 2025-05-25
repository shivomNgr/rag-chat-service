RAG Chat Storage Microservice
A production-ready FastAPI-based microservice for managing chat sessions and messages in a Retrieval-Augmented Generation (RAG) chatbot system. It provides secure, scalable APIs for session management, message storage, and retrieval, with PostgreSQL integration.
Features

Create, update, delete, and mark chat sessions as favorites
Store and retrieve messages with optional context (e.g., RAG data)
API key authentication and rate limiting (10 requests/minute/IP)
Centralized logging for debugging
Dockerized deployment with PostgreSQL and pgAdmin
Comprehensive unit tests with pytest and pytest-asyncio

Tech Stack

Backend: Python 3.11, FastAPI
Database: PostgreSQL 15 (via asyncpg)
ORM: SQLAlchemy (async)
Environment: python-dotenv
Rate Limiting: slowapi
Testing: pytest, pytest-asyncio, httpx
Deployment: Docker, Docker Compose, uvicorn

Prerequisites

Python 3.11+
PostgreSQL 15
Docker and Docker Compose (for containerized setup)
Git

Installation
Using Docker (Recommended)

Clone the Repository:
git clone https://github.com/shivomNgr/rag-chat-service.git
cd rag-chat-service


Set Up Environment Variables:

Copy .env.example to .env:cp .env.example .env  # On Windows: copy .env.example .env


Update .env with your credentials:DATABASE_URL=postgresql+asyncpg://user:password@db:5432/rag_chat
API_KEY=your-secret-api-key
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin




Run with Docker Compose:
docker-compose up --build -d


Application: http://localhost:8000
Swagger UI: http://localhost:8000/docs
pgAdmin: http://localhost:5050 (login with PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD)



Manual Installation

Clone the Repository:
git clone https://github.com/shivomNgr/rag-chat-service.git
cd rag-chat-service


Set Up Virtual Environment:
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Set Up Environment Variables:

Copy .env.example to .env and update:cp .env.example .env  # On Windows: copy .env.example .env

DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/rag_chat
API_KEY=your-secret-api-key




Set Up PostgreSQL:

Ensure PostgreSQL is running.
Create database:psql -U user -c "CREATE DATABASE rag_chat;"




Run the Application:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


Application: http://localhost:8000
Swagger UI: http://localhost:8000/docs



Testing
Run unit tests to verify functionality:

Ensure dependencies are installed (requirements.txt).
Execute tests:pytest app/tests/ -v



API Endpoints
All endpoints require X-API-Key header for authentication. Key endpoints:

POST /chat/sessions: Create a new chat session
GET /chat/sessions/{session_id}: Retrieve session details
PUT /chat/sessions/{session_id}: Update session name or favorite status
DELETE /chat/sessions/{session_id}: Delete session and associated messages
POST /chat/sessions/{session_id}/messages: Add a message
GET /chat/sessions/{session_id}/messages?page={page}&page_size={page_size}: Retrieve paginated messages
GET /health: Check service health

Detailed API docs: http://localhost:8000/docs
Project Structure
rag_chat_service/
├── app/
│   ├── database/       # Database models and utilities
│   ├── models/        # Pydantic models
│   ├── repositories/  # Data access logic
│   ├── routes/        # API endpoints
│   ├── tests/         # Unit tests
│   ├── utils/         # Helper functions
│   ├── main.py        # FastAPI app entry point
├── .env.example       # Example environment variables
├── docker-compose.yml # Docker Compose configuration
├── README.md          # Project documentation
├── requirements.txt   # Python dependencies

Notes

Ensure PostgreSQL is accessible before starting the application.
Include API_KEY in X-API-Key header for all requests.
Rate limiting: 10 requests/minute/IP.
Logs: Written to app.log and console.

Contributing

Fork the repository.
Create a feature branch: git checkout -b feature/your-feature
Commit changes: git commit -m "Add your feature"
Push branch: git push origin feature/your-feature
Open a Pull Request.

License
MIT License
Contact

Maintainer: Shivom Sharma
Email: shivom.sharma@nagarro.com
GitHub: shivomNgr

