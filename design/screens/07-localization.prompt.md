# Localization / Supplier Finder

## Purpose
Find local suppliers for woodworking materials.

---

## Pencil Prompt

```
Design a local supplier finder interface for KerfOS - woodworking materials.

Layout:
- Top section: Location input
  - Zip code input with autocomplete
  - "Use My Location" button with GPS icon
  - Radius slider (5-100 miles)

- Filter bar:
  - Category chips: Plywood, Hardware, Tools, Finishes, Hardwood
  - Store type chips: Big Box, Hardware Chain, Specialty, Lumber Yard

- Main area: Store cards
  - Store card design:
    - Store logo and name
    - Distance in miles
    - Address with directions link
    - Phone number (clickable)
    - Price tier indicator (Budget/Mid/Premium)
    - Category tags
    - "View Inventory" button
    - Store hours indicator (Open/Closed)

- Tabs: All Stores | By Category | Price Comparison

- Price comparison tab:
  - Item search input
  - Comparison table with prices from different stores
  - In-stock indicators
  - "Add to Cart" buttons

- Map view option:
  - Toggle between list and map
  - Markers for store locations
  - Current location blue dot
  - Click marker for store card popup

Style: Google Maps meets Yelp for woodworking
Cards: Clean, scannable, with quick action buttons
Mobile: Swipeable store cards with bottom sheet details
```

---

## Design Tokens Used

- Primary: #2563EB
- Secondary: #059669
- Accent: #D97706
- Open indicator: #10B981
- Closed indicator: #DC2626

---

## Components

- Location input
- Filter chips
- Store cards
- Price comparison table
- Map view
- List/map toggle

---

## Interactions

- Use GPS location
- Search by zip
- Filter stores
- Toggle list/map view
- Click for directions
- Price comparison
