# Quickstart Guide: Todo Frontend Application

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Git for version control

## Setup Instructions

### 1. Clone and Initialize
```bash
# Create new Next.js project
npx create-next-app@latest todo-frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"

cd todo-frontend
```

### 2. Install Dependencies
```bash
npm install @better-auth/react @better-auth/client
```

### 3. Project Structure
Create the following directory structure:
```
src/
├── app/              # Next.js App Router pages
│   ├── layout.tsx
│   ├── page.tsx
│   ├── signin/
│   │   └── page.tsx
│   ├── signup/
│   │   └── page.tsx
│   └── tasks/
│       └── page.tsx
├── components/       # Reusable UI components
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── TaskCard.tsx
│   ├── TaskForm.tsx
│   ├── Filters.tsx
│   └── Button.tsx
├── lib/             # Utility functions
│   ├── api.ts
│   └── auth.ts
└── styles/          # Global styles
    └── globals.css
```

### 4. Environment Variables
Create a `.env.local` file:
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret-key-here
```

### 5. Configuration Files
Configure `tailwind.config.js` to use light parrot green as primary color:
```js
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#78FF00', // light parrot green
        }
      }
    },
  },
  plugins: [],
}
```

## Development Workflow

### Running the Application
```bash
npm run dev
```

### Key Development Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter

## Architecture Patterns

### Component Structure
- Server Components by default (for static content)
- Client Components only where interactivity is required (using 'use client' directive)

### API Integration
- All backend communication through `/lib/api.ts`
- Automatic JWT token attachment
- Global 401 handling

### Authentication Flow
- Better Auth integration
- Protected routes using middleware
- Session management utilities