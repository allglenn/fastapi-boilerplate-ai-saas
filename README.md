# FastAPI React Docker Boilerplate

A modern full-stack boilerplate featuring FastAPI, React, PostgreSQL, and Docker. This project includes both an admin interface and a client application, with built-in authentication and email functionality.

## 🚀 Features

- **Backend (FastAPI)**
  - FastAPI framework for high performance
  - PostgreSQL database integration
  - JWT authentication
  - Email service integration
  - Docker containerization
- 

- **Frontend**
  - React with TypeScript
  - Vite for fast development
  - Admin interface (port 3001)
  - Client interface (port 3000)
  - Hot Module Replacement (HMR)

- **Development Tools**
  - Docker & Docker Compose setup
  - MailCatcher for email testing
  - Auto-reload for both frontend and backend
  - CORS configured for development

## 🛠 Prerequisites

- Docker and Docker Compose
- Node.js (for local development)
- Python 3.8+ (for local development)

## 🚦 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/allglenn/fastapi-boilerplate-ai-saas.git
   cd fastapi-boilerplate-ai-saas
   ```

2. **Environment Setup**
   ```bash
   # Copy the example env file
   cp api/.env.example api/.env
   ```

3. **Start the Application**
   ```bash
   docker-compose up --build
   ```

4. **Access the Applications**
   - Admin Interface: http://localhost:3001
   - Client Interface: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - MailCatcher Interface: http://localhost:1080

## 📁 Project Structure

```
├── api/                 # FastAPI backend
├── ui-admin/           # Admin interface (React)
├── client/            # Client interface (React)
├── docker-compose.yml  # Docker composition
└── README.md
```

## 🔌 Available Services

| Service      | Port  | Description                    |
|--------------|-------|--------------------------------|
| FastAPI      | 8000  | Backend API                    |
| Admin UI     | 3001  | Administration interface       |
| Client UI    | 3000  | Client application            |
| PostgreSQL   | 5432  | Database                      |
| MailCatcher  | 1080  | Email testing interface       |

## 💻 Development

### API Development

The FastAPI backend includes:
- Authentication endpoints
- User management
- Email service integration
- PostgreSQL database with automatic migrations

### Frontend Development

Both frontend applications (admin and client) feature:
- React with TypeScript
- Vite development server
- Hot Module Replacement
- Environment variable support
- CORS configuration for development

## 🔒 Environment Variables

Key environment variables:

```env
DOMAIN_NAME=http://localhost:3000
DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
SECRET_KEY=your-secret-key
```

## 📧 Email Testing

The boilerplate includes MailCatcher for email testing:
1. Emails are captured at http://localhost:1080
2. SMTP server runs on port 1025

## 🐳 Docker Commands

```bash
# Build and start all services
docker-compose up --build

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild a specific service
docker-compose build <service-name>
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

