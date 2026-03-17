# Feedback Components

## Purpose
Core feedback system for KerfOS.

---

## Pencil Prompt

```
Design feedback components for KerfOS.

1. Toast notifications:
   - Success (green)
   - Error (red)
   - Warning (yellow)
   - Info (blue)
   - Position: top-right
   - Auto-dismiss after 5s
   - Action button optional

2. Loading states:
   - Spinner
   - Skeleton loader
   - Progress bar
   - Shimmer effect

3. Empty states:
   - Icon
   - Message
   - Call to action button

4. Error states:
   - Icon
   - Error message
   - Retry button
   - Support link

5. Success states:
   - Checkmark animation
   - Success message
   - Next action
```

---

## Toast Notifications

```
┌─────────────────────────────────────┐
│ ✓ Project saved successfully    ✕  │
└─────────────────────────────────────┘
```

- Position: top-right
- Width: 360px max
- Animation: slide in from right
- Auto-dismiss: 5 seconds

### Variants

| Type | Icon | Background | Border |
|------|------|------------|--------|
| Success | ✓ | #D1FAE5 | #10B981 |
| Error | ✕ | #FEE2E2 | #DC2626 |
| Warning | ⚠ | #FEF3C7 | #D97706 |
| Info | ℹ | #DBEAFE | #3B82F6 |

---

## Loading States

### Spinner
```
        ◠
       ╱ ╲
      ◡   ◞
       ╲ ╱
        ◡
```

- Size: 24px, 32px, 48px
- Color: #2563EB
- Animation: rotate 1s linear infinite

### Skeleton Loader
```
┌─────────────────────────────────────┐
│ ███████████████████                 │
│ ████████████████████████████████    │
│ ████████████████                    │
└─────────────────────────────────────┘
```

- Background: #F3F4F6
- Shimmer: linear gradient animation

---

## Empty States

```
      ┌───────────┐
      │           │
      │    📦     │
      │           │
      └───────────┘

   No projects yet
   
Create your first project
   [Create Project]
```

- Centered on container
- Large icon (64px)
- Title: 18px semibold
- Description: 14px regular
- CTA button

---

## Error States

```
      ┌───────────┐
      │           │
      │    ⚠️     │
      │           │
      └───────────┘

   Something went wrong
   
Unable to load projects. Please
try again or contact support.

   [Retry] [Contact Support]
```

- Similar to empty state but red accent
- Retry button primary action
- Support link secondary

---

## Success States

```
      ┌───────────┐
      │           │
      │    ✓      │
      │           │
      └───────────┘

   Project created!
   
Your project is ready to edit.

   [Open Project]
```

- Checkmark animation (spring)
- Green accent color
- Next action button

---

## Design Tokens

| Property | Value |
|----------|-------|
| Toast duration | 5s |
| Animation duration | 250ms |
| Icon size | 24px |
| Large icon size | 64px |
