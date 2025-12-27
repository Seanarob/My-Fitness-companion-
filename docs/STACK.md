# FIT-AI Next Gen - Technology Stack

## Overview
Locked technology stack for FIT-AI Next Gen rebuild. All decisions are final to prevent churn during development.

## Backend

**Framework:** FastAPI (Python 3.11+)
- Local Port: `8000`
- Base URL (local): `http://localhost:8000`
- API Docs: `http://localhost:8000/docs` (Swagger UI)

**Database:** MongoDB
- Local Port: `27017`
- Connection String (local): `mongodb://localhost:27017/fitai`
- ODM: Motor (async MongoDB driver for Python)

**Authentication:** JWT (JSON Web Tokens)
- Algorithm: HS256
- Access token expiration: 15 minutes
- Refresh token expiration: 7 days
- Token storage: HTTP-only cookies for web, Keychain for iOS

**AI Service:** OpenAI API
- Models: GPT-4o (coaching interactions), GPT-4o-mini (structured parsing)
- Usage: Async calls via `openai` Python library

## iOS Client

**Framework:** SwiftUI
- Minimum iOS: 17.0
- Language: Swift 5.9+
- Architecture: MVVM

**Backend Communication (Local Development):**
- **iOS Simulator:** `http://localhost:8000`
- **Physical Device:** `http://[YOUR_COMPUTER_IP]:8000` (requires network access)
- **Network Library:** URLSession (native) or async/await HTTP client
- **Environment Variable:** `API_BASE_URL` in build schemes (Debug/Release)

**Example Local URLs:**
- Simulator: `http://localhost:8000/api/v1/auth/login`
- Device: `http://192.168.1.100:8000/api/v1/auth/login`

## Web Frontend

**Framework:** Vite + React
- Local Port: `5173`
- Base URL (local): `http://localhost:5173`
- Build Tool: Vite 5.x
- React Version: 18.x
- TypeScript: Yes

**State Management:** Zustand (lightweight, no boilerplate)

**HTTP Client:** Axios (with interceptors for JWT refresh)

**Backend Communication (Local Development):**
- API Proxy: Vite proxy configured to forward `/api/*` to `http://localhost:8000`
- Direct calls: `http://localhost:8000/api/v1/*`

**Styling:** Tailwind CSS (utility-first, fast development)

## Development Workflow

### Local Development Setup

1. **MongoDB:** Run locally on port 27017
2. **Backend:** FastAPI on port 8000
3. **Web Frontend:** Vite dev server on port 5173
4. **iOS:** Xcode preview/build, connects to backend on localhost:8000 (simulator) or [IP]:8000 (device)

### Port Summary
- MongoDB: `27017`
- FastAPI Backend: `8000`
- Vite Web Frontend: `5173`

### CORS Configuration
Backend must allow:
- Web frontend: `http://localhost:5173`
- iOS Simulator: `http://localhost:8000` (same-origin, no CORS)
- iOS Device: `http://[COMPUTER_IP]:8000` (CORS headers required)

## Environment Variables

### Backend (.env)
```
MONGODB_URL=mongodb://localhost:27017/fitai
OPENAI_API_KEY=sk-...
JWT_SECRET=...
JWT_ALGORITHM=HS256
ENVIRONMENT=development
```

### iOS (Xcode Scheme Environment Variables)
```
API_BASE_URL=http://localhost:8000  # Debug
API_BASE_URL=https://api.fitai.app  # Release
```

### Web Frontend (.env.local)
```
VITE_API_BASE_URL=http://localhost:8000
VITE_ENVIRONMENT=development
```

## Deployment Targets (Future)

- **Backend:** TBD (Docker + cloud provider)
- **MongoDB:** TBD (MongoDB Atlas or self-hosted)
- **Web Frontend:** TBD (Vercel/Netlify static hosting)
- **iOS:** App Store

---

*Stack locked as of 2025-12-26. Do not modify without explicit approval.*

