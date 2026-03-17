# Cut List Export

## Purpose
Generate and export optimized cut lists for cabinet projects.

---

## Pencil Prompt

```
Design a cut list generation and export interface for KerfOS.

Layout:
- Top section: Project summary
  - Project name and thumbnail
  - Total sheets needed
  - Waste percentage visualization
  - Cost breakdown card

- Main area: Cut list table
  - Sortable columns: Part Name, Quantity, Dimensions, Material, Edge Banding
  - Grouped by material type (collapsible sections)
  - Selectable rows with bulk actions
  - Search/filter within list

- Right sidebar: Preview panel
  - 2D sheet layout preview
  - Sheet navigation (Sheet 1, 2, 3...)
  - Zoom controls
  - Print preview button

- Bottom actions:
  - Export buttons: PDF, CSV, DXF, G-code
  - Share link button
  - Print button
  - Save to project button

- G-code specific modal:
  - Machine profile selector (ShopBot, Shapeoko, X-Carve)
  - Feed rate settings
  - Tab/bridge configuration
  - Preview generated code
  - Download button

Style: Technical but approachable, like professional CAD software
Tables: Alternating row colors, sticky headers
Exports: Clear icon buttons with format labels
```

---

## Design Tokens Used

- Primary: #2563EB
- Secondary: #059669
- Monospace: JetBrains Mono (for measurements)
- Table row alt: #F3F4F6

---

## Components

- Project summary card
- Data table
- Sheet preview panel
- Export buttons
- G-code modal
- Waste visualization

---

## Interactions

- Sort columns
- Select rows
- Navigate sheets
- Zoom preview
- Export to multiple formats
