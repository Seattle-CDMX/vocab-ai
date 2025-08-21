# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Start development server:**
```bash
npm run dev
```

**Build for production:**
```bash
npm run build
```

**Build for development:**
```bash
npm run build:dev
```

**Lint code:**
```bash
npm run lint
```

**Preview production build:**
```bash
npm run preview
```

## Architecture Overview

This is a React-based phrasal verb learning application built with Vite, TypeScript, and shadcn/ui components.

**Key Technologies:**
- **Frontend**: React 18 + TypeScript + Vite
- **UI Framework**: shadcn/ui components + Tailwind CSS
- **Routing**: React Router v6
- **State Management**: React Query + React hooks
- **Build Tool**: Vite with SWC

**Application Structure:**

**Pages (`src/pages/`):**
- `Index.tsx` - Landing page with Hero component
- `Study.tsx` - Study session with flashcard practice
- `Dashboard.tsx` - Main dashboard showing phrasal verb collection with SRS levels
- `FlashCard.tsx` - Individual flashcard view for specific verbs
- `NotFound.tsx` - 404 error page

**Core Components (`src/components/`):**
- `Hero.tsx` - Landing page hero section
- `StudyCard.tsx` - Interactive study card for practicing phrasal verbs
- `ProgressBar.tsx` - Progress visualization for study sessions
- `ui/` - Complete shadcn/ui component library

**Data Model:**
The app uses a Spaced Repetition System (SRS) with "neuron growth" levels:
- `srsLevel: 0` - Locked verbs (not yet unlocked)
- `srsLevel: 1-9` - Progressive learning levels with visual neuron growth indicators
- Difficulty levels: `beginner`, `intermediate`, `advanced`

**Routing Structure:**
- `/` - Landing page
- `/study` - Study session
- `/dashboard` - Main dashboard
- `/flashcard/:id` - Individual flashcard

**State Management:**
- React Query for data fetching/caching
- Local state with React hooks
- No global state management (Redux/Zustand) currently implemented

**Key Features:**
- Interactive flashcard system
- SRS-based learning progression
- Visual neuron growth indicators
- Difficulty-based categorization
- Search and filtering capabilities
- Responsive design with Tailwind CSS

## Important Notes

- The app currently uses mock data in components - no backend integration yet
- All phrasal verb data is stored as constants in component files
- The SRS system is visual only - no actual spaced repetition scheduling implemented
- Built for Lovable.dev platform with automatic deployments