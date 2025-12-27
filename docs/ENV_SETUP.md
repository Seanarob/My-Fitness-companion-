# Environment Setup Guide

## Overview
This guide explains where environment files live, how to configure them, and how to keep secrets secure.

## File Locations

### Backend
- **Environment file:** `backend/.env`
- **Example file:** `.env.example` (at repo root)
- **Usage:** FastAPI reads from `backend/.env` using `python-dotenv`

### Frontend (Web)
- **Environment file:** `frontend/.env.local` (for local development)
- **Environment file:** `frontend/.env.production` (for production builds)
- **Example file:** `frontend/.env.example` (to be created)
- **Usage:** Vite automatically loads `.env.local` in development

### iOS
- **Environment variables:** Configured in Xcode Scheme settings (Debug/Release)
- **File location:** Not stored in files, set in Xcode → Edit Scheme → Run → Arguments → Environment Variables
- **Variable name:** `API_BASE_URL`

## Setup Steps

### 1. Backend Setup

```bash
# Copy example to backend directory
cp .env.example backend/.env

# Edit backend/.env and fill in actual values
# - MONGODB_URI: Your MongoDB connection string
# - OPENAI_API_KEY: Your OpenAI API key from https://platform.openai.com/api-keys
# - JWT_SECRET: Generate a secure random string (32+ characters)
# - FRONTEND_API_BASE_URL: http://localhost:5173 (for local dev)
# - IOS_API_BASE_URL: http://localhost:8000 (for local dev)
```

**Generate JWT_SECRET:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Or
openssl rand -hex 32
```

### 2. Frontend Setup

```bash
# Create frontend/.env.local
cd frontend
cat > .env.local << EOF
VITE_API_BASE_URL=http://localhost:8000
VITE_ENVIRONMENT=development
EOF
```

### 3. iOS Setup

1. Open `ios/FitAI.xcodeproj` in Xcode
2. Product → Scheme → Edit Scheme...
3. Select "Run" → "Arguments" tab
4. Under "Environment Variables", click "+"
5. Add: `API_BASE_URL` = `http://localhost:8000` (Debug)
6. Duplicate scheme for Release and set: `API_BASE_URL` = `https://api.fitai.app`

## Running Locally

### Prerequisites
- MongoDB running on port 27017 (or update MONGODB_URI)
- Python 3.11+ installed
- Node.js 18+ installed (for frontend)

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Ensure .env file exists (copy from .env.example if needed)
# Load environment variables are handled by python-dotenv in config.py

# Run development server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Ensure .env.local exists with VITE_API_BASE_URL

# Run development server
npm run dev
# Server runs on http://localhost:5173
```

### iOS

1. Open `ios/FitAI.xcodeproj` in Xcode
2. Ensure API_BASE_URL environment variable is set in scheme
3. Build and run (Cmd+R) or use Preview (Cmd+Option+P)

### MongoDB

```bash
# macOS (using Homebrew)
brew services start mongodb-community

# Or run manually
mongod --config /usr/local/etc/mongod.conf

# Verify connection
mongosh mongodb://localhost:27017/fitai
```

## Keeping Secrets Out of Git

### .gitignore Rules

All environment files must be in `.gitignore`:

```gitignore
# Environment files
.env
.env.local
.env.production
.env.*.local
backend/.env
frontend/.env.local
frontend/.env.production

# But allow example files
!.env.example
```

### Best Practices

1. **Never commit secrets:**
   - ❌ Never commit `.env` files
   - ❌ Never commit `.env.local` files
   - ✅ Only commit `.env.example` with placeholders

2. **Example files are safe:**
   - `.env.example` contains only placeholder values
   - Safe to commit and share

3. **Team sharing:**
   - Share actual secrets via secure password manager (1Password, LastPass, etc.)
   - Or use team environment variable management tool
   - Never share secrets in Slack, email, or GitHub issues

4. **CI/CD (Future):**
   - Use environment variables in CI/CD platform (GitHub Actions secrets, etc.)
   - Never hardcode secrets in workflow files

5. **Verify before commit:**
   ```bash
   # Check what's being committed
   git status
   git diff
   
   # Verify .gitignore is working
   git check-ignore -v backend/.env
   ```

## Environment Variable Reference

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/fitai` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `JWT_SECRET` | Secret key for JWT signing | Random 32+ character string |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ENVIRONMENT` | Environment name | `development`, `production` |
| `FRONTEND_API_BASE_URL` | Frontend URL for CORS | `http://localhost:5173` |
| `IOS_API_BASE_URL` | iOS API URL for CORS | `http://localhost:8000` |

### Frontend (.env.local)

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API base URL | `http://localhost:8000` |
| `VITE_ENVIRONMENT` | Environment name | `development` |

### iOS (Xcode Environment Variables)

| Variable | Description | Example |
|----------|-------------|---------|
| `API_BASE_URL` | Backend API base URL | `http://localhost:8000` (Debug) |

## Troubleshooting

### Backend can't read .env
- Ensure `backend/.env` exists (not just `.env` at root)
- Check file is not in `.gitignore` (should be ignored, but file must exist locally)
- Verify `python-dotenv` is installed

### Frontend can't connect to backend
- Check `VITE_API_BASE_URL` in `frontend/.env.local`
- Ensure backend is running on port 8000
- Check CORS configuration in backend

### iOS can't connect to backend
- Verify `API_BASE_URL` in Xcode scheme environment variables
- For physical device: Use computer's IP address, not `localhost`
- Check network connectivity

---

*Last updated: 2025-12-26*

