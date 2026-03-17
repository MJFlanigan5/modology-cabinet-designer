# Hardware Finder

## Purpose
Find and purchase cabinet hardware from multiple suppliers.

---

## Pencil Prompt

```
Design a hardware finder interface for KerfOS - cabinet hardware shopping.

Layout:
- Left sidebar (280px):
  - Category tree navigation
  - Active filters display
  - Price range slider
  - Supplier filter checkboxes

- Top bar:
  - Search input with autocomplete
  - View toggle (grid/list)
  - Sort dropdown

- Main area:
  - Product grid (4 columns desktop, 2 mobile)
  - Each product card:
    - Product image (200px)
    - Product name (2 lines max)
    - Price with supplier badge
    - Rating stars
    - "Add to Project" button
    - "Compare" checkbox
    - "Buy" link to supplier

- Comparison bar (bottom, when items selected):
  - Shows selected products side by side
  - Compare specifications table
  - Clear all / Remove individual items

- Quick view modal:
  - Product details
  - Specifications table
  - Compatible cabinets from user's projects
  - Similar products carousel

Style: E-commerce product grid with clean, minimal aesthetic
Suppliers: Show supplier logos (Rockler, Home Depot, Lowe's, etc.)
```

---

## Design Tokens Used

- Primary: #2563EB
- Secondary: #059669
- Background: #F9FAFB
- Card: #FFFFFF

---

## Components

- Category tree
- Product cards
- Filter sidebar
- Comparison bar
- Quick view modal
- Rating stars
- Supplier badges

---

## Interactions

- Search with autocomplete
- Filter selection
- Grid/list view toggle
- Compare products
- Quick view modal
- Add to project
