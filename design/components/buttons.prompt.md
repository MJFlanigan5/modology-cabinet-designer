# Button Components

## Purpose
Core button system for KerfOS.

---

## Pencil Prompt

```
Design a button component system for KerfOS.

Button variants:
1. Primary (filled blue): Main actions like "Save", "Export", "Create"
2. Secondary (outline): Secondary actions like "Cancel", "Back"
3. Ghost (text only): Tertiary actions like "Learn More"
4. Danger (red): Destructive actions like "Delete", "Remove"
5. Success (green): Positive actions like "Complete", "Approve"

Button sizes:
- Small (32px): Compact UIs, tables
- Medium (40px): Default
- Large (48px): Hero actions, mobile

States:
- Default, Hover, Active, Disabled, Loading

Include:
- Icon buttons (icon only)
- Icon + text combinations
- Button groups
- Split buttons with dropdown
```

---

## Design Tokens

| Variant | Background | Text | Border | Hover Background |
|---------|------------|------|--------|------------------|
| Primary | #2563EB | #FFFFFF | none | #1D4ED8 |
| Secondary | transparent | #2563EB | #2563EB | #DBEAFE |
| Ghost | transparent | #2563EB | none | #F3F4F6 |
| Danger | #DC2626 | #FFFFFF | none | #B91C1C |
| Success | #10B981 | #FFFFFF | none | #059669 |

---

## Sizes

| Size | Height | Padding | Font Size |
|------|--------|---------|----------|
| Small | 32px | 8px 12px | 14px |
| Medium | 40px | 10px 16px | 16px |
| Large | 48px | 12px 24px | 18px |

---

## States

- **Default**: Normal appearance
- **Hover**: Darker background, cursor pointer
- **Active**: Even darker, pressed effect
- **Disabled**: 50% opacity, no pointer events
- **Loading**: Spinner, text hidden

---

## Accessibility

- Minimum 44px touch target for mobile
- Focus ring: 2px solid #2563EB, 2px offset
- Keyboard navigable
- aria-label for icon buttons
