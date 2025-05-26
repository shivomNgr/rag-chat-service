# RAG Chat Storage Microservice

A production-ready FastAPI-based microservice for managing chat sessions and messages in a Retrieval-Augmented Generation (RAG) chatbot system. It provides secure, scalable APIs for session management, message storage, and retrieval, with PostgreSQL integration.

## Features
- Create, update, delete chat sessions
- Mark sessions as favorites
- Store and retrieve messages with RAG context
- API key authentication
- Rate limiting (10 requests/minute/IP)
- Centralized logging
- Dockerized deployment
- Comprehensive unit tests

## Tech Stack
- **Backend**: Python 3.11, FastAPI
- **Database**: PostgreSQL 15 (via asyncpg)
- **ORM**: SQLAlchemy (async)
- **Environment**: python-dotenv
- **Rate Limiting**: slowapi
- **Testing**: pytest, pytest-asyncio, httpx
- **Deployment**: Docker, Docker Compose, uvicorn

## Prerequisites
- Python 3.11+
- PostgreSQL 15
- Docker (for containerized setup)
- Git

## Installation

### Docker Setup (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/shivomNgr/rag-chat-service.git
cd rag-chat-service 
```

2. Setup environment Variables:
```bash
cp .env.example .env
# For Windows: copy .env.example .env
```
Update .env with your credentials:
  ```bash
  DATABASE_URL=postgresql+asyncpg://user:password@db:5432/rag_chat
  API_KEY=your-secret-api-key
  PGADMIN_DEFAULT_EMAIL=admin@admin.com
  PGADMIN_DEFAULT_PASSWORD=admin
  ```
3. Run with Docker Compose:
```bash
docker-compose up --build -d
```
**Access**:
- Application: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- pgAdmin: http://localhost:5050 (login with PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD)

## Manual Installation
1: Clone Repository:
```bash
git clone https://github.com/shivomNgr/rag-chat-service.git
cd rag-chat-service
```
2: Set Up Virtual Environment:
```bash
python -m venv env
source env/bin/activate
# Windows: env\Scripts\activate
```
3: Install dependencies:
```bash
pip install -r requirements.txt
```
4: Set Up Environment Variables:
Copy .env.example to .env and update:
```bash
cp .env.example .env  # On Windows: copy .env.example .env
```
Add below variables:
```bash
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/rag_chat
API_KEY=your-secret-api-key
```
5: Set Up PostgreSQL:
Ensure PostgreSQL is running.
Create database:
```bash
psql -U user -c "CREATE DATABASE rag_chat;"
```
5: Run application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Application: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

## Testing
Run unit tests to verify functionality:
### All Tests (recommended):
```bash
  pytest app/tests/ -v
```
### Individual Test Files:
```bash
pytest app/tests/test_message.py -v
pytest app/tests/test_session.py -v
```

**Note**: Tests cover health checks, session CRUD operations, message addition, and retrieval. Ensure the database is configured (DATABASE_URL in .env) before running tests.


## API Endpoints
All endpoints require X-API-Key header for authentication. Key endpoints:
- `POST /chat/sessions`: Create a new chat session
- `GET /chat/sessions/{session_id}`: Retrieve session details
- `PUT /chat/sessions/{session_id}`: Update session name or favorite status
- `DELETE /chat/sessions/{session_id}`: Delete session and associated messages
- `POST /chat/sessions/{session_id}/messages`: Add a message
- `GET /chat/sessions/{session_id}/messages?page={page}&page_size={page_size}`: Retrieve paginated messages
- `GET /health`: Check service health

Full docs at: http://localhost:8000/docs

## Project Structure
```bash
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
```
## Notes
- Ensure PostgreSQL is accessible before starting the application.
- Include API_KEY in X-API-Key header for all requests.
- Rate limiting: 10 requests/minute/IP.
- Logs: Written to app.log and console.

## CORS Configuration
In production, configure Cross-Origin Resource Sharing (CORS) to allow requests only from trusted origins (e.g., your frontend application). The service uses FastAPI's CORSMiddleware for CORS settings, defined in app/main.py.
* To update CORS settings for production:
  - Open app/main.py
  - Locate the CORSMiddleware configuration:
  ```bash
  from fastapi.middleware.cors import CORSMiddleware

  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:3000"],  # Update this for production
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```
  * Replace allow_origins with your production frontend domains:
    ```bash
    allow_origins=["https://your-frontend.com", "https://*.your-frontend.com"]
    ```
     - Use specific domains (e.g., **https://app.example.com**) instead of wildcards (*) for security.
     - For subdomains, use **https://*.example.com**.

  * Optionally, restrict allow_methods and allow_headers for stricter control:
  ```bash
  allow_methods=["GET", "POST", "PUT", "DELETE"],
  allow_headers=["Authorization", "Content-Type", "X-API-Key"],
  ```
  * Restart the application to apply changes:
  ```bash
  docker-compose restart  # If using Docker
  # OR
  uvicorn app.main:app --host 0.0.0.0 --port 8000
  ```

  **Note**:
  Avoid using allow_origins=["*"] in production, as it allows requests from any origin, posing a security risk.

## Contributing
- Fork the repository.
-  Create a feature branch: git checkout -b feature/your-feature
- Commit changes: git commit -m "Add your feature"
- Push branch: git push origin feature/your-feature
- Open a Pull Request.

## License
MIT License

## Contact
- Maintainer: Shivom Sharma
- Email: shivom.sharma@nagarro.com
- GitHub: shivomNgr
