# FIT-AI Next Gen - Technology Decisions

## Overview
This document explains why each technology choice was made and how it prevents churn during development. All decisions are locked to maintain velocity.

## Backend: FastAPI

**Decision:** FastAPI (Python) instead of Node.js/Express, Go, or Rails.

**Rationale:**
1. **OpenAI Integration:** Native Python library support, no wrapper complexity
2. **Async-First:** Built for async/await, critical for AI API calls and MongoDB async operations
3. **Type Safety:** Pydantic models provide runtime validation and automatic API docs (Swagger)
4. **Rapid Development:** Less boilerplate than Django, more structured than Flask
5. **Team Familiarity:** Python is widely known, easier onboarding

**Churn Prevention:** Type-safe request/response models catch errors at development time. Automatic OpenAPI docs prevent API contract drift between frontend and backend.

## Database: MongoDB

**Decision:** MongoDB instead of PostgreSQL, MySQL, or SQLite.

**Rationale:**
1. **Flexible Schema:** User profiles, workout templates, and nutrition logs have varying structures
2. **Document Model:** Natural fit for JSON-based workout/exercise data
3. **Async Support:** Motor driver aligns with FastAPI's async architecture
4. **Scalability:** Horizontal scaling easier than SQL for future growth
5. **Nested Data:** Workout sets, exercise history stored naturally without joins

**Churn Prevention:** Schema changes don't require migrations. Can evolve data models incrementally as requirements clarify.

## Authentication: JWT

**Decision:** JWT tokens instead of sessions, OAuth-only, or API keys.

**Rationale:**
1. **Stateless:** FastAPI doesn't need session storage, simplifies scaling
2. **Cross-Platform:** Works identically for iOS (native) and web (HTTP-only cookies)
3. **Refresh Pattern:** Short-lived access tokens + long-lived refresh tokens provide security without UX friction
4. **Standard:** Widely supported, no custom auth flow needed
5. **Mobile-Friendly:** Keychain storage on iOS, no cookies to manage

**Churn Prevention:** Single auth pattern works for both clients. Refresh token rotation prevents re-auth interruptions.

## AI Service: OpenAI

**Decision:** OpenAI API instead of Anthropic Claude, local models, or multiple providers.

**Rationale:**
1. **GPT-4o Quality:** Best-in-class for conversational coaching and structured parsing
2. **Single API:** Reduces integration complexity and vendor management
3. **Reliability:** Production-grade uptime and rate limits
4. **Voice Parsing:** Whisper API available for future voice workout input
5. **Cost Predictable:** Usage-based pricing scales with growth

**Churn Prevention:** No vendor switching later. OpenAI API is stable and well-documented.

## iOS: SwiftUI

**Decision:** SwiftUI instead of UIKit, React Native, or Flutter.

**Rationale:**
1. **Native Performance:** Zero bridge overhead, direct system integration
2. **Modern Declarative:** Less code, easier state management than UIKit
3. **Preview System:** Instant UI feedback during development
4. **iOS 17+ Features:** Latest APIs, modern design patterns
5. **Team Focus:** Swift-only codebase, no cross-platform tradeoffs

**Churn Prevention:** Native app feels polished from day one. No need to switch frameworks mid-development.

## Web Frontend: Vite + React

**Decision:** Vite + React instead of Next.js, Remix, or Svelte.

**Rationale:**
1. **Development Speed:** Vite HMR is instant, faster than Next.js dev server
2. **Simplicity:** No SSR complexity for dashboard-style app (no SEO needed)
3. **TypeScript Support:** First-class TypeScript, catches errors early
4. **Bundle Size:** Smaller output than Next.js, faster load times
5. **React Ecosystem:** Largest library ecosystem, easy to find solutions
6. **Single-Page App:** Perfect for authenticated dashboard/mobile companion view

**Churn Prevention:** Vite dev experience is best-in-class. No need to add SSR later since web is secondary to iOS app. React's stability ensures long-term maintainability.

## State Management: Zustand (Web)

**Decision:** Zustand instead of Redux, Context API, or Jotai.

**Rationale:**
1. **Minimal Boilerplate:** ~10 lines vs 100+ for Redux
2. **TypeScript Native:** Full type inference, no extra configuration
3. **Performance:** Selective re-renders, no Provider hell
4. **Small Bundle:** ~1KB, negligible impact
5. **Flexibility:** Can use with or without middleware

**Churn Prevention:** Simple enough that we won't outgrow it. No Redux complexity to maintain.

## HTTP Client: Axios (Web) / URLSession (iOS)

**Decision:** Axios for web, URLSession for iOS (native).

**Rationale:**
1. **Web:** Interceptors for JWT refresh, request/response transformation, widely adopted
2. **iOS:** Native URLSession, no third-party dependency, async/await support
3. **Consistency:** Both support interceptors, error handling patterns align

**Churn Prevention:** Native iOS client avoids dependency bloat. Axios is battle-tested on web.

## Styling: Tailwind CSS (Web)

**Decision:** Tailwind CSS instead of CSS Modules, styled-components, or Material-UI.

**Rationale:**
1. **Speed:** Utility classes, no context switching to CSS files
2. **Consistency:** Design system via config, prevents style drift
3. **Bundle Size:** PurgeCSS removes unused styles automatically
4. **No Naming Conflicts:** Utility classes don't collide
5. **iOS Alignment:** Can mirror design tokens between Tailwind config and iOS colors/fonts

**Churn Prevention:** Design system defined once in Tailwind config. No need to refactor styles later.

## Type Safety: Everywhere

**Decision:** Pydantic (backend), TypeScript (web), Swift types (iOS).

**Rationale:**
1. **Catch Errors Early:** Type mismatches fail at compile/dev time, not production
2. **API Contracts:** Shared types prevent frontend/backend drift
3. **Refactoring Safety:** Types ensure changes propagate correctly
4. **Documentation:** Types serve as inline docs

**Churn Prevention:** Type system prevents entire classes of bugs. No runtime surprises from malformed data.

## Local Development: Localhost + Proxy

**Decision:** All services run locally with port-based routing.

**Rationale:**
1. **No Cloud Dependency:** Develop offline, no API costs during development
2. **Fast Iteration:** No network latency, instant feedback
3. **Debugging:** Full access to logs, breakpoints, database inspection
4. **Cost:** Zero cloud spend during development phase

**Churn Prevention:** Local-first approach means we can develop without infrastructure setup blocking us. Can deploy later when needed.

---

*All decisions locked to prevent analysis paralysis and ensure consistent development velocity.*

