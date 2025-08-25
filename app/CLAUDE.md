# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- `npm run dev` - Start development server with Turbopack for fast builds
- `npm run build` - Build the application for production
- `npm start` - Start the production server
- `npm run lint` - Run ESLint to check code quality

## Project Architecture

This is a Next.js 15 application implementing a LiveKit video conferencing room management system.

### Key Components

- **App Router Structure**: Uses Next.js App Router with TypeScript
- **Main Room Interface** (`app/page.tsx`): Primary video conferencing interface with room management
- **Study Page** (`app/study/page.tsx`): Voice card practice interface with phrasal verb learning
- **Dashboard** (`app/dashboard/page.tsx`): User progress tracking and statistics
- **Slides Presentation** (`app/slides/page.tsx`): Reveal.js presentation system with Mermaid diagrams
- **API Routes** (`app/api/token/route.ts`): Handles LiveKit token generation, room listing, and deletion

### LiveKit Integration

The application uses LiveKit for real-time video conferencing:

- **Client Libraries**: `@livekit/components-react`, `livekit-client`
- **Server SDK**: `livekit-server-sdk` for room management
- **Required Environment Variables**:
  - `LIVEKIT_API_KEY`
  - `LIVEKIT_API_SECRET` 
  - `LIVEKIT_URL`
  - `NEXT_PUBLIC_LIVEKIT_URL`
  - `APP_PASSWORD` - Password for app-wide protection

### API Endpoints

- `GET /api/token?room={name}&username={user}&voiceCardData={encoded_json}` - Generate access token for room
  - `voiceCardData` (optional): URL-encoded JSON containing voice card data that will be embedded in the token metadata
  - The metadata is accessible to LiveKit agents for context-aware voice interactions
- `POST /api/token` - List all active rooms
- `DELETE /api/token?room={name}` - Delete room and disconnect participants
- `POST /api/auth` - Authenticate with app password

### Password Protection System

The application implements comprehensive password protection using:

- **Middleware** (`middleware.ts`): Intercepts all requests and redirects unauthenticated users to login
- **Login Page** (`app/login/page.tsx`): Modern, responsive authentication interface
- **Auth API** (`app/api/auth/route.ts`): Server-side password validation with secure cookie management
- **Session Management**: HTTP-only cookies for secure, persistent authentication (7-day expiration)
- **Deployment Ready**: Works seamlessly with Vercel and other hosting platforms

**Security Features:**
- Server-side password validation
- HTTP-only cookies prevent XSS attacks
- Secure flag in production
- SameSite protection
- Complete app lockdown until authenticated

### Technology Stack

- **Framework**: Next.js 15 with App Router
- **Runtime**: React 19
- **Styling**: Tailwind CSS 4, inline styles for LiveKit components
- **TypeScript**: Full TypeScript configuration
- **Fonts**: Geist Sans and Geist Mono from Google Fonts

### Key Features

- **Password Protection**: App-wide authentication using middleware and secure cookies
- Real-time video conferencing with adaptive streaming
- Room creation and management interface
- Participant management and room cleanup
- Session management with localStorage integration
- Room deletion with participant disconnection
- **Voice Card Integration**: Passes voice card data via token metadata to LiveKit agents for context-aware voice practice
- **Audio-Only Mode**: VoiceCard component requests only microphone permission for voice-based learning
- **Presentation System**: Reveal.js slides with Mermaid diagram support for technical presentations
- **Spaced Repetition Learning**: Built-in SRS system for phrasal verb practice with progress tracking

### Development Notes

- Uses Turbopack for fast development builds
- ESLint configured with Next.js recommended settings
- Strict TypeScript configuration enabled
- No test framework currently configured

### Common Deployment Issues

#### React Unescaped Entities Error
When deploying to Vercel, you may encounter ESLint errors about unescaped entities in JSX:
- Apostrophes (`'`) should be replaced with `&apos;`
- Double quotes (`"`) should be replaced with `&quot;`
- This is enforced by the `react/no-unescaped-entities` ESLint rule
- The build will fail on Vercel if these aren't properly escaped, even if they work locally

#### TypeScript Module Declaration Issues
When using external libraries like `reveal.js` without built-in TypeScript support:
- Install corresponding `@types` packages: `npm install --save-dev @types/reveal.js`
- For missing type declarations, create a `.d.ts` file or use `declare module` statements
- This prevents TypeScript compilation errors during Vercel builds

#### Dependencies and Package Management
Current key dependencies include:
- **Presentation**: `reveal.js`, `mermaid` for slides and diagrams
- **LiveKit**: `@livekit/components-react`, `livekit-client`, `livekit-server-sdk`
- **UI Components**: `@radix-ui/react-slot`, `lucide-react`, `sonner`
- **Styling**: `tailwindcss`, `class-variance-authority`, `clsx`, `tailwind-merge`