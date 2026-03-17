# Cabinet Builder (Main Workspace)

## Purpose
Primary workspace for designing cabinets with 3D preview, component palette, and properties panel.

---

## Pencil Prompt

```
Design a professional cabinet builder workspace for KerfOS - DIY woodworkers.

Layout (Desktop):
- Left sidebar (300px): Component palette
  - Drag-and-drop cabinet components (boxes, doors, drawers, shelves)
  - Component categories with expandable sections
  - Search/filter components
  - Recent components section

- Center canvas (flexible): 
  - 3D preview viewport with orbit controls
  - Grid background with measurement markers
  - Zoom controls (zoom in/out, fit to screen, reset view)
  - View mode toggle (3D, 2D Top, 2D Front, 2D Side)
  - Component selection highlights with transform handles

- Right sidebar (320px): Properties panel
  - Selected component properties (dimensions, material, position)
  - Material selector with preview thumbnails
  - Hardware recommendations (context-aware)
  - Quick actions: Duplicate, Delete, Lock position
  - Cost preview card

- Bottom panel (collapsible):
  - Cut list preview with material breakdown
  - Timeline/version history
  - Notes and comments

Style: Professional CAD tool meets modern SaaS
Features: 
- Real-time 3D preview with Three.js style rendering
- Drag indicators when hovering
- Snap-to-grid visual feedback
- Measurement tooltips on hover
- Undo/redo toolbar
- Save status indicator
```

---

## Design Tokens Used

- Primary: #2563EB
- Secondary: #059669
- Accent: #D97706
- Background: #F9FAFB
- Canvas background: #1F2937 (dark for contrast)

---

## Components

- Component palette sidebar
- 3D viewport canvas
- Properties panel
- Cut list panel
- Toolbar
- Zoom controls
- View mode toggle

---

## Interactions

- Drag and drop components
- Click to select
- Transform handles for resize/rotate
- Zoom/pan/rotate 3D view
- Property editing
- Undo/redo
