# Modal Components

## Purpose
Core modal system for KerfOS.

---

## Pencil Prompt

```
Design modal component system for KerfOS.

Modal types:
1. Alert/Confirm (simple message, OK/Cancel)
2. Form modal (larger, form content)
3. Full-screen modal (mobile)
4. Side panel modal (slides from right)
5. Bottom sheet (mobile)

Modal anatomy:
- Header with title
- Close button (X)
- Body content
- Footer with actions
- Overlay backdrop

Features:
- Dismissible by clicking outside
- Escape key to close
- Focus trap inside modal
- Scroll lock on body
- Responsive sizing
```

---

## Modal Types

### Alert/Confirm
```
┌─────────────────────────────┐
│ Delete Project?          ✕ │
├─────────────────────────────┤
│                             │
│ Are you sure you want to   │
│ delete "Kitchen Remodel"?  │
│ This action cannot be      │
│ undone.                    │
│                             │
├─────────────────────────────┤
│         [Cancel] [Delete]   │
└─────────────────────────────┘
```

- Width: 400px max
- Centered on screen

---

### Form Modal
```
┌─────────────────────────────┐
│ New Project              ✕ │
├─────────────────────────────┤
│                             │
│ Project Name *             │
│ ┌─────────────────────────┐ │
│ │ Untitled Project        │ │
│ └─────────────────────────┘ │
│                             │
│ Description                 │
│ ┌─────────────────────────┐ │
│ │                         │ │
│ │                         │ │
│ └─────────────────────────┘ │
│                             │
├─────────────────────────────┤
│         [Cancel] [Create]   │
└─────────────────────────────┘
```

- Width: 500-600px
- Centered on screen

---

### Side Panel
```
┌─────────────────────────────┬──────────────┐
│                             │ Settings   ✕ │
│                             │              │
│      Main Content           │ Name         │
│      (dimmed)               │ ┌──────────┐ │
│                             │ │          │ │
│                             │ └──────────┘ │
│                             │              │
│                             │ [Save]       │
└─────────────────────────────┴──────────────┘
```

- Width: 400px
- Slides from right

---

### Bottom Sheet (Mobile)
```
┌─────────────────────────────┐
│                             │
│      Main Content           │
│                             │
├─────────────────────────────┤
│ ───────                     │ <- Handle
│ Share Options               │
│ ┌─────────────────────────┐ │
│ │ 📷 Share to Instagram   │ │
│ ├─────────────────────────┤ │
│ │ 📘 Share to Facebook    │ │
│ ├─────────────────────────┤ │
│ │ 📋 Copy Link            │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘
```

- Slides from bottom
- Dismiss on swipe down

---

## Design Tokens

| Property | Value |
|----------|-------|
| Overlay | rgba(0, 0, 0, 0.5) |
| Background | #FFFFFF |
| Border Radius | 16px |
| Shadow | xl |
| Padding | 24px |

---

## Accessibility

- Focus trap when modal open
- Escape key to close
- aria-modal="true"
- aria-labelledby pointing to title
