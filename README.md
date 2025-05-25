RAG Chat Storage Microservice

Introduction
The RAG Chat Storage Microservice is a production-ready backend service designed to store and manage chat sessions and messages for a Retrieval-Augmented Generation (RAG) based chatbot system. It provides APIs to create and manage chat sessions, store messages with optional context, rename sessions, mark sessions as favorites, delete sessions with cascading message deletion, and retrieve paginated message histories. The service is built with scalability, security, and best practices in mind, featuring API key authentication, rate limiting, centralized logging, and Dockerized deployment.
Technology Stack
The microservice is built using the following technologies:

Python 3.11: Core programming language for the backend.
FastAPI: High-performance web framework for building APIs with automatic Swagger documentation.
PostgreSQL: Relational database for storing chat sessions and messages, accessed via asyncpg.
SQLAlchemy (Async): ORM for database operations with asynchronous support.
python-dotenv: For managing environment variables.
slowapi: For rate limiting to prevent API abuse.
pytest & pytest-asyncio: For unit testing with asynchronous support.
Docker & docker-compose: For containerized deployment, including PostgreSQL and pgAdmin.
uvicorn: ASGI server for running the FastAPI application.

Installation
Using Docker
The recommended way to run the service is with Docker, which sets up the application, PostgreSQL database, and pgAdmin for easy database management.

Clone the Repository:
git clone <repository-url>
cd rag_chat_service


Set Up Environment Variables:

Copy the .env.example file to .env:cp .env.example .env


Update .env with your configuration:DATABASE_URL=postgresql+asyncpg://user:password@db:5432/rag_chat
API_KEY=your-secret-api-key




Run with Docker Compose:

Start the services (application, PostgreSQL, and pgAdmin):docker-compose up --build


The application will be available at http://localhost:8000.
Access Swagger UI for API documentation at http://localhost:8000/docs.
Access pgAdmin at http://localhost:5050 (login with admin@admin.com and password admin).



Manual Installation
If you prefer to run the service manually without Docker, follow these steps:

Clone the Repository:
git clone <repository-url>
cd rag_chat_service


Set Up a Virtual Environment:

Create and activate a virtual environment:python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate




Install Dependencies:

Install required packages from requirements.txt:pip install -r requirements.txt




Set Up Environment Variables:

Copy .env.example to .env and update it:cp .env.example .env

DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/rag_chat
API_KEY=your-secret-api-key




Set Up PostgreSQL:

Ensure a PostgreSQL server is running locally or remotely.
Create a database named rag_chat:psql -U user -c "CREATE DATABASE rag_chat;"




Run the Application:

Start the FastAPI application with uvicorn:uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


Access the application at http://localhost:8000 and Swagger UI at http://localhost:8000/docs.



Testing
The project includes unit tests to verify core functionality. To run the tests:

Ensure Dependencies Are Installed:

If using the virtual environment, ensure pytest and pytest-asyncio are installed (included in requirements.txt).


Run Tests:

Execute the test suite with verbose output:pytest app/tests/test_chat.py -v


This runs tests for health checks, session creation, updates, deletion, message addition, and retrieval.



API Endpoints
The microservice provides the following APIs (all protected with API key authentication via X-API-Key header):

POST /chat/sessions: Create a new chat session.
GET /chat/sessions/{session_id}: Retrieve a session by ID.
PUT /chat/sessions/{session_id}: Update session name or favorite status.
DELETE /chat/sessions/{session_id}: Delete a session and its messages.
POST /chat/sessions/{session_id}/messages: Add a message to a session.
GET /chat/sessions/{session_id}/messages?page={page}&page_size={page_size}: Retrieve paginated messages for a session.
GET /health: Check service health.

For detailed API documentation, visit http://localhost:8000/docs when the application is running.
Notes

Ensure PostgreSQL is running and accessible before starting the application.
The API_KEY in .env must be included in the X-API-Key header for all API requests.
Rate limiting is enforced (10 requests per minute per IP) to prevent abuse.
Logs are written to app.log and the console for debugging.

