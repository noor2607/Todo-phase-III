# Todo AI Chatbot

This project consists of a Next.js frontend deployed on Vercel and a FastAPI backend deployed on Hugging Face Spaces.

## Project Structure

- `frontend/` - Next.js frontend application
- `backend_todo_chatbot/` - FastAPI backend application for AI chat functionality

## Overview

This is a full-stack todo application with AI chatbot functionality. The project uses a dual-backend approach:
- Main backend for authentication and task management
- Separate AI chatbot backend for natural language processing

## Configuration

### Frontend (Deployed at https://todo-phase-iii.vercel.app/)

The frontend is configured to connect to two different backends using separate environment variables:

1. **Main Backend** (Authentication & Task Management):
   - Uses `NEXT_PUBLIC_API_BASE_URL` environment variable
   - Handles user authentication, registration, login, and task CRUD operations

2. **Chatbot Backend** (AI Chat Functionality):
   - Uses `NEXT_PUBLIC_BACKEND_URL` environment variable
   - Currently set to: `https://larebnoor-todo-chatbot.hf.space/`
   - Handles AI chat functionality and natural language processing

### Backend (Deployed at https://larebnoor-todo-chatbot.hf.space)

The chatbot backend is configured with CORS to allow requests from:
- `https://todo-phase-iii.vercel.app` (production frontend)
- `http://localhost:3000` (local development)
- `http://localhost:3001` (alternative local port)
- `http://localhost:8000` (backend local server)

## Files Using Each Backend

### Main Backend (`NEXT_PUBLIC_API_BASE_URL`)
- `frontend/app/signin/page.tsx` - Login functionality
- `frontend/app/signup/page.tsx` - Registration functionality
- `frontend/lib/api.ts` - Base API client (default for most requests)
- `frontend/services/taskService.ts` - Task management operations

### Chatbot Backend (`NEXT_PUBLIC_BACKEND_URL`)
- `frontend/components/ChatInterface.tsx` - AI chat functionality

## Environment Variables

### Frontend
- `NEXT_PUBLIC_API_BASE_URL`: Points to the main backend API
- `NEXT_PUBLIC_BACKEND_URL`: Points to the chatbot backend API (currently https://larebnoor-todo-chatbot.hf.space/)

### Backend
- `COHERE_API_KEY`: API key for Cohere integration
- `JWT_SECRET`: Secret for JWT token generation
- `DATABASE_URL`: Database connection string

## Deployment

### Backend Deployment to Hugging Face Spaces
The backend can be deployed to Hugging Face Spaces using the provided Dockerfile.

### Frontend Deployment to Vercel
The frontend can be deployed to Vercel with both environment variables properly configured.