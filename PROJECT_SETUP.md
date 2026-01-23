# Todo AI Chatbot - Project Setup Documentation

## Overview

This project has a dual backend setup:
1. Main backend for authentication and task management
2. Separate chatbot backend for AI functionality

## Environment Variables

### Frontend Configuration

The frontend uses two different backend URLs:

1. **Main Backend (Authentication & Tasks)**:
   - Variable: `NEXT_PUBLIC_API_BASE_URL`
   - Purpose: Handles user authentication, registration, login, and task management
   - Example: `https://main-backend-domain.com`

2. **Chatbot Backend (AI Chat)**:
   - Variable: `NEXT_PUBLIC_BACKEND_URL`
   - Purpose: Handles AI chat functionality and natural language processing
   - Currently set to: `https://larebnoor-todo-chatbot.hf.space/`

### Current Configuration

For the deployed application at `https://todo-phase-iii.vercel.app/`:
- Authentication & Task Management: Uses the original backend URL
- AI Chat Functionality: Uses `https://larebnoor-todo-chatbot.hf.space/`

## Files Using Each Backend

### Main Backend (`NEXT_PUBLIC_API_BASE_URL`)
- `frontend/app/signin/page.tsx` - Login functionality
- `frontend/app/signup/page.tsx` - Registration functionality
- `frontend/lib/api.ts` - Base API client (default for most requests)
- `frontend/services/taskService.ts` - Task management operations

### Chatbot Backend (`NEXT_PUBLIC_BACKEND_URL`)
- `frontend/components/ChatInterface.tsx` - AI chat functionality

## Backend Configuration

### Chatbot Backend (Hugging Face Spaces)
- Located in `backend_todo_chatbot/` directory
- Deployed at `https://larebnoor-todo-chatbot.hf.space`
- Includes CORS configuration to accept requests from `https://todo-phase-iii.vercel.app`
- Built with FastAPI and includes AI agent functionality

## Deployment

### Frontend (Vercel)
Ensure both environment variables are set in Vercel dashboard:
- `NEXT_PUBLIC_API_BASE_URL`: Main backend URL
- `NEXT_PUBLIC_BACKEND_URL`: Chatbot backend URL

### Backend (Hugging Face Spaces)
Deploy the `backend_todo_chatbot/` directory with the provided Dockerfile.