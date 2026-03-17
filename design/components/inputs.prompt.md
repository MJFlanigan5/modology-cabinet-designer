# Form Input Components

## Purpose
Core form input system for KerfOS.

---

## Pencil Prompt

```
Design form input components for KerfOS.

Input types:
1. Text input (single line)
2. Textarea (multi-line)
3. Number input with steppers
4. Dimension input (with unit selector)
5. Search input (with icon)
6. Dropdown select
7. Multi-select with chips
8. Checkbox
9. Radio button
10. Toggle switch
11. Date picker
12. File upload (drag and drop)

States:
- Default, Focused, Filled, Error, Disabled

Features:
- Labels (above input)
- Helper text (below input)
- Error messages (below input, red)
- Character count
- Required indicator (*)
```

---

## Design Tokens

| State | Border | Background | Label Color |
|-------|--------|------------|-------------|
| Default | #E5E7EB | #FFFFFF | #374151 |
| Focused | #2563EB | #FFFFFF | #2563EB |
| Filled | #E5E7EB | #F9FAFB | #374151 |
| Error | #DC2626 | #FEE2E2 | #DC2626 |
| Disabled | #E5E7EB | #F3F4F6 | #9CA3AF |

---

## Input Anatomy

```
[Label *]                    <- Label (14px, semibold)
┌─────────────────────────┐
│ Placeholder text        │ <- Input (16px, regular)
└─────────────────────────┘
Helper text goes here        <- Helper (12px, regular, gray)
```

---

## Dimension Input

Specialized input for measurements:
- Number field
- Unit dropdown (in, ft, mm, cm, m)
- Fraction support (1/2, 1/4, 3/8)

---

## File Upload

- Drag and drop zone
- Click to browse
- Progress bar for uploads
- File type icons
- Preview thumbnails

---

## Accessibility

- Label association (for/id)
- Error announced by screen reader
- Required indicator accessible
- Focus visible
