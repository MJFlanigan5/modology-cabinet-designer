# Cabinet Builder - Mobile Version

## Purpose
Mobile-optimized cabinet builder interface for tablets and phones.

---

## Pencil Prompt

```
Design a mobile cabinet builder interface for KerfOS on tablets and phones.

Layout:
- Top bar: Back button, project name, save status, more menu
- Main area: 3D preview (touch to rotate, pinch to zoom)
- Bottom tab bar: Components | Preview | Properties | Export
- Floating action button: Add component

Components Tab:
- Scrollable list of component cards with thumbnails
- Tap to add, long-press for options

Preview Tab:
- Full-screen 3D view with gesture controls
- Tap to select, double-tap to edit

Properties Tab:
- Scrollable form with all properties
- Large touch targets (44px minimum)
- Steppers for numeric values

Export Tab:
- Export options as large buttons
- Preview thumbnails for each format
```

---

## Design Tokens Used

- Touch targets: 44px minimum
- Font sizes: Larger for readability
- High contrast for workshop visibility
- Dark mode support

---

## Components

- Top navigation bar
- Bottom tab bar
- Component cards
- 3D preview
- Property form
- Export buttons
- Floating action button

---

## Interactions

- Swipe between tabs
- Pinch to zoom
- Touch to rotate 3D
- Tap to select
- Long-press for options
