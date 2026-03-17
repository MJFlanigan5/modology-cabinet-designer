# Card Components

## Purpose
Core card system for KerfOS.

---

## Pencil Prompt

```
Design card component system for KerfOS.

Card types:
1. Project card (thumbnail, title, stats)
2. Template card (preview, name, difficulty)
3. Product card (image, price, supplier)
4. Stat card (icon, number, label)
5. Issue card (severity, description, action)
6. Suggestion card (before/after, action buttons)

Card anatomy:
- Header (optional)
- Body content
- Footer actions (optional)
- Hover state
- Selected state

Features:
- Clickable entire card
- Action buttons on hover
- Loading skeleton
- Empty state
```

---

## Design Tokens

| Property | Value |
|----------|-------|
| Background | #FFFFFF |
| Border | #E5E7EB |
| Border Radius | 12px |
| Shadow | 0 4px 6px -1px rgb(0 0 0 / 0.1) |
| Hover Shadow | 0 10px 15px -3px rgb(0 0 0 / 0.1) |
| Padding | 16px |

---

## Card Types

### Project Card
```
┌─────────────────────┐
│ [Thumbnail 16:9]    │
│                     │
├─────────────────────┤
│ Project Name        │
│ Last edited: 2h ago │
│ ────────────────── │
│ 📦 12 parts  $234   │
└─────────────────────┘
```

### Stat Card
```
┌─────────────────────┐
│ 🔧 Icon             │
│                     │
│ 24                  │ <- Large number
│ Total Projects      │ <- Label
└─────────────────────┘
```

### Issue Card
```
┌─────────────────────┐
│ ⚠️ Warning          │ <- Severity badge
│ Door overlap        │ <- Title
│ The cabinet door... │ <- Description
│ [Fix Now]           │ <- Action button
└─────────────────────┘
```

---

## States

- **Default**: White background, light shadow
- **Hover**: Elevated shadow, subtle border
- **Selected**: Blue border, light blue background
- **Loading**: Skeleton with shimmer animation

---

## Accessibility

- Entire card clickable (via nested button)
- Focus visible on card
- aria-label for action buttons
