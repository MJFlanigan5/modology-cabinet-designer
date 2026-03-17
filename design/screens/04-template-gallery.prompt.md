# Template Gallery

## Purpose
Browse and select pre-built cabinet configurations to jumpstart projects.

---

## Pencil Prompt

```
Design a template gallery for KerfOS - pre-built cabinet configurations.

Layout:
- Top search and filter bar
  - Search input with icon
  - Filter chips: Kitchen, Bathroom, Garage, Office, Living Room
  - Sort dropdown: Popular, Newest, Easiest First

- Main grid (responsive):
  - Template cards (300px width, variable height)
  - Each card shows:
    - 3D preview thumbnail (16:9 aspect ratio)
    - Template name and category badge
    - Difficulty indicator (Beginner/Intermediate/Advanced)
    - Estimated time and cost
    - Star rating from community
    - "Use Template" button on hover

- Sidebar filters (desktop):
  - Style filters: Shaker, Flat-panel, Raised-panel, Modern
  - Difficulty level checkboxes
  - Price range slider
  - Room type checkboxes

Style: Pinterest-style grid with woodworking aesthetic
Cards: Hover effects showing quick preview and action buttons
Empty state: "No templates match your filters" with clear filters button
```

---

## Design Tokens Used

- Primary: #2563EB
- Secondary: #059669
- Accent: #D97706
- Card background: #FFFFFF
- Shadow: md

---

## Components

- Search input
- Filter chips
- Template cards
- Sidebar filters
- Star rating
- Difficulty badges
- Category badges

---

## Interactions

- Search with autocomplete
- Filter selection
- Card hover effects
- Click to preview template
- "Use Template" action
