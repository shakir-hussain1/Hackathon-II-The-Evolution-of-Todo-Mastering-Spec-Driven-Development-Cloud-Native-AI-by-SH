# Prompt History Record: ui-state-management Skill

## Creation Date
2026-01-11

## Skill Type
Frontend Quality Skill

## Purpose
Standardizes UI states across the application ensuring consistent UX through proper loading, empty, and error states.

## Key Functions
1. Loading state definition and validation
2. Empty state design and messaging
3. Error state implementation review
4. UX pattern consistency enforcement
5. Silent failure prevention

## Required States
- **Loading:** Spinners, skeletons for all async ops
- **Empty:** Helpful message + CTA for zero items
- **Error:** User-friendly message + retry option
- **Success:** Confirmation feedback for actions

## Common Issues
- Blank screens while loading
- Silent error failures
- Unhelpful empty states
- Technical error messages
- No action feedback

## UI Patterns
- Loading: Skeleton screens, spinners, progress
- Empty: Illustration + message + CTA button
- Error: Icon + message + retry button
- Optimistic updates with rollback

## Usage Patterns
- After component implementation
- When adding async operations
- For UX consistency reviews
- Before user testing
- Quality assurance checks

## Integration Points
- Works with frontend-ui-dashboard
- Validates frontend-api-integration
- Supports error-normalization-handling
- Feeds quality-readiness-validation

## Success Metrics
- **Loading States:** 100% async ops
- **Empty States:** 100% list views
- **Error States:** 100% errors displayed
- **Silent Failures:** 0
- **User Feedback:** 100% actions
