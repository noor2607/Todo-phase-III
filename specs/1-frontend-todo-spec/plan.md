# Implementation Plan: Todo Frontend Application

## Technical Context
- Frontend Framework: Next.js 14+ with App Router
- Styling: Tailwind CSS
- Authentication: Better Auth frontend
- API Communication: Centralized API client in /lib/api.ts
- Theme Color: Light parrot green (primary action color)
- Architecture: Server Components by default, Client Components only for interactivity

## Constitution Check
- All API calls must go through /lib/api.ts (✓ Per constitution)
- JWT tokens must be automatically attached (✓ Per constitution)
- User data isolation enforced (✓ Per constitution)
- No hardcoded user IDs (✓ Per constitution)
- Server Components by default (✓ Per constitution)
- Client Components only for interactivity (✓ Per constitution)

## Phase 0: Research & Resolution

### Research Tasks
- Research optimal Next.js 14+ project structure with App Router
- Research Better Auth integration patterns with Next.js App Router
- Research best practices for centralized API clients in Next.js
- Research responsive design patterns with Tailwind CSS
- Research accessibility patterns for task management applications

### Decision Summary
- Will use App Router file structure as per constitution
- Will implement Better Auth with client components only where needed
- Will create centralized API client with automatic JWT handling
- Will use Tailwind for responsive design
- Will implement proper accessibility attributes

### Artifacts Created
- research.md: Research findings and decisions
- data-model.md: Task and User Session entity definitions
- contracts/: API contract for task operations
- quickstart.md: Setup and development workflow guide

## Phase 1: Project Setup & Configuration

### 1. Initialize Next.js Project
- Create new Next.js 14+ project with App Router
- Configure TypeScript with appropriate tsconfig settings
- Set up ESLint and Prettier with appropriate configurations
- Install required dependencies: react, react-dom, next, typescript, @types/react, @types/node

### 2. Install UI and Authentication Dependencies
- Install Tailwind CSS and configure for Next.js
- Install Better Auth frontend package
- Install any additional UI utility libraries as needed
- Configure PostCSS for Tailwind processing

### 3. Project Structure Setup
- Create directory structure following constitution:
  - app/ (Next.js App Router)
  - components/ (UI components)
  - lib/ (utility functions and API client)
  - public/ (static assets)

## Phase 2: Global Layout (Header, Footer, Theme, Tailwind Setup)

### 4. Configure Tailwind CSS
- Set up theme with light parrot green as primary color
- Define color palette in tailwind.config.js
- Configure variants and plugins as needed
- Set up base, component, and utility styles

### 5. Create Root Layout
- Implement app/layout.tsx with base HTML structure
- Add global CSS imports
- Set up providers (Better Auth provider, etc.)
- Implement base styling and responsive utilities

### 6. Build Header Component
- Create Header server component in components/
- Include logo/app name and navigation links
- Add Home, Features, Sign In, Sign Up links
- Ensure header is visible on all pages
- Make responsive for mobile and desktop

### 7. Build Footer Component
- Create Footer server component in components/
- Include About, Features, Contact, GitHub links
- Add copyright text
- Ensure consistent across all pages
- Make responsive for mobile and desktop

## Phase 3: Public Pages (Home, Sign In, Sign Up)

### 8. Create Home Page
- Implement app/page.tsx (home page)
- Add hero section explaining the app
- Include feature highlights (CRUD tasks, user isolation, fast, secure)
- Add call-to-action buttons: Sign Up / Sign In
- Include showcase screenshot placeholders
- Ensure responsive design

### 9. Create Sign In Page
- Implement app/signin/page.tsx
- Build sign in form using Better Auth frontend SDK
- Add clean form validation
- Implement loading and error states
- Include proper redirects after success

### 10. Create Sign Up Page
- Implement app/signup/page.tsx
- Build sign up form using Better Auth frontend SDK
- Add clean form validation
- Implement loading and error states
- Include proper redirects after success

## Phase 4: Authentication Flow (Better Auth Frontend)

### 11. Configure Better Auth
- Set up Better Auth provider in root layout
- Configure authentication client-side
- Implement session management utilities
- Create helper functions for auth state checking

### 12. Create Authentication Utilities
- Build auth.ts in lib/ directory
- Implement functions to check auth status
- Create utilities for protecting routes
- Add redirect logic for auth-gated pages

### 13. Implement Route Protection
- Create middleware or higher-order components for protected routes
- Ensure /tasks page requires authentication
- Redirect unauthenticated users to sign-in
- Handle session expiry gracefully

## Phase 5: API Client Implementation

### 14. Create Centralized API Client
- Build lib/api.ts with centralized API wrapper
- Implement automatic JWT token attachment
- Add global handling for 401 Unauthorized responses
- Create typed responses using TypeScript interfaces
- Add proper error handling and logging

### 15. Implement API Endpoints Functions
- Create functions for task CRUD operations
- Implement user authentication API calls
- Add functions for filtering and sorting tasks
- Ensure all API calls go through the centralized client

## Phase 6: Protected Tasks Page with CRUD UI

### 16. Create Tasks Page Structure
- Implement app/tasks/page.tsx as protected page
- Fetch tasks via API client
- Create layout for task list display
- Add navigation from auth pages to tasks page

### 17. Build Task Components
- Create TaskCard component for displaying tasks
- Build TaskForm component for task creation/modification
- Create Filters component for filtering and sorting
- Build Button component with parrot green variant

### 18. Implement Task CRUD Functionality
- Enable task creation through modal/form
- Implement task update functionality (inline or modal)
- Add task deletion with confirmation
- Create toggle for completed state
- Ensure all operations use the API client

## Phase 7: State Handling, Loading, Error & Empty States

### 19. Implement Loading States
- Add loading skeletons for task lists
- Create loading states for API operations
- Implement optimistic updates where appropriate
- Add proper loading indicators to UI

### 20. Handle Error States
- Create user-friendly error messages
- Implement global error handling
- Add specific error handling for API failures
- Include network error handling

### 21. Handle Empty States
- Design empty state for task lists
- Add guidance for first-time users
- Create clear call-to-actions for empty states
- Ensure empty states are responsive

### 22. State Management Implementation
- Use React state for UI interactions (modals, inputs, filters)
- Implement client state for filter and sort settings
- Ensure server data fetching is preferred
- Add proper state synchronization with API

## Phase 8: Final Polish, Responsiveness & Accessibility

### 23. Responsive Design Implementation
- Apply responsive classes to all components
- Test mobile, tablet, and desktop layouts
- Optimize touch targets for mobile devices
- Ensure proper navigation on all screen sizes

### 24. Accessibility Improvements
- Add proper ARIA attributes to interactive elements
- Ensure keyboard navigation works for all components
- Implement proper focus management
- Add semantic HTML elements where appropriate

### 25. UI Polish
- Refine hover and focus states
- Ensure consistent spacing and typography
- Apply parrot green theme consistently
- Optimize performance and loading times

### 26. Testing and Quality Assurance
- Test all user flows from specification
- Verify all authentication flows work correctly
- Ensure API integration functions properly
- Test responsive design across devices
- Validate accessibility compliance

## Critical Files to be Modified
- app/layout.tsx
- app/page.tsx
- app/signin/page.tsx
- app/signup/page.tsx
- app/tasks/page.tsx
- components/Header.tsx
- components/Footer.tsx
- components/TaskCard.tsx
- components/TaskForm.tsx
- components/Filters.tsx
- components/Button.tsx
- lib/api.ts
- lib/auth.ts
- tailwind.config.js
- package.json

## Verification Steps
1. Start the development server and verify basic navigation
2. Test authentication flow (sign up, sign in, protected routes)
3. Verify task CRUD operations work end-to-end
4. Test filtering and sorting functionality
5. Validate responsive design on different screen sizes
6. Check accessibility features and keyboard navigation
7. Confirm API client properly handles authentication tokens
8. Verify error handling and loading states work properly