# Mobile Companion App

## Purpose
Mobile app for woodworkers to use KerfOS in the workshop.

---

## Pencil Prompt

```
Design a mobile companion app for KerfOS - cabinet builders in the workshop.

Home Screen:
- Top: Greeting with user name, today's projects
- Quick actions grid (2x2):
  - View Cut Lists
  - Scan Barcode
  - Material Calculator
  - Take Photo
- Active projects carousel
- Shopping list summary card
- Offline mode indicator

Bottom Navigation:
- Home | Projects | Tools | Profile

Cut List View:
- Material tabs (Plywood, MDF, Hardware)
- Each item shows:
  - Part name
  - Dimensions (large text)
  - Check off checkbox
  - Notes indicator
- Progress bar showing completion
- "Mark All Done" button

Barcode Scanner:
- Camera viewfinder with scanning frame
- Product info overlay when detected
- "Add to Inventory" button
- Manual search fallback

Material Calculator:
- Quick input fields (length, width, quantity)
- Material type selector
- Result: Sheets needed, cost estimate
- "Add to Shopping List" button

Photo Notes:
- Camera capture
- Annotate with drawings
- Voice note option
- Attach to project

Style: High contrast, large text, workshop-friendly
Dark mode: Default (easier to see in bright workshop)
Offline: Clear indicator when offline
```

---

## Design Tokens Used

- Touch targets: 44px minimum
- Font sizes: Larger (18px base)
- High contrast
- Dark mode by default
- Offline indicator: #D97706

---

## Components

- Home screen
- Bottom navigation
- Cut list view
- Barcode scanner
- Material calculator
- Photo notes

---

## Interactions

- Tab navigation
- Scan barcode
- Calculate materials
- Take photo
- Annotate photo
- Offline sync
