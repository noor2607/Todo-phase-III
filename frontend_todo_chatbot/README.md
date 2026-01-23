# Todo AI Chatbot Frontend

This is the frontend component for the Todo AI Chatbot application. It provides a user-friendly interface for interacting with the AI-powered task management system.

## Features

- Dashboard view with AI assistant icon
- Chat interface for natural language task management
- Real-time conversation history
- Secure JWT-based authentication
- Responsive design for all device sizes

## Tech Stack

- Next.js 14: React framework with App Router
- React 18: JavaScript library for building user interfaces
- Tailwind CSS: Utility-first CSS framework (used in combination with custom CSS)

## Installation

1. Clone the repository
2. Navigate to the frontend directory
3. Install the required packages:

```bash
npm install
```

## Running the Application

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

## Project Structure

- `app/`: Next.js app directory with page components
- `src/components/`: Reusable React components
- `src/pages/`: Page-level components
- `src/styles/`: Global and component-specific styles
- `public/`: Static assets

## Components

- `TodoChat`: Main chat interface component
- `Dashboard`: Home page with bot icon trigger
- Various UI elements for messaging, controls, and feedback

## API Integration

The frontend communicates with the backend API at `/api/{user_id}/chat` to process natural language requests and manage tasks.

## Authentication

The application expects JWT tokens to be available through the authentication system and passes them with each API request to the backend.