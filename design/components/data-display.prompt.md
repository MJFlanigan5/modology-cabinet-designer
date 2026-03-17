# Data Display Components

## Purpose
Core data display system for KerfOS.

---

## Pencil Prompt

```
Design data display components for KerfOS.

1. Tables:
   - Sortable columns
   - Row selection
   - Pagination
   - Empty state
   - Loading state

2. Lists:
   - Simple list
   - List with actions
   - Expandable list

3. Badges:
   - Status badges (success, warning, error)
   - Category badges
   - Count badges

4. Progress:
   - Progress bar
   - Circular progress
   - Step progress

5. Charts:
   - Bar chart (cost comparison)
   - Pie/donut chart (material breakdown)
   - Line chart (project timeline)

6. Tooltips:
   - Info tooltip
   - Hover tooltip
   - Context menu
```

---

## Tables

```
┌────────────────────────────────────────────────────────┐
│ Part Name     │ Qty │ Dimensions    │ Material         │
├────────────────────────────────────────────────────────┤
│ Side Panel    │  2  │ 36" x 24"    │ 3/4" Plywood  ▾ │
│ Shelf         │  4  │ 12" x 24"    │ 3/4" Plywood     │
│ Door          │  2  │ 18" x 30"    │ 3/4" MDF         │
├────────────────────────────────────────────────────────┤
│                     Showing 1-10 of 45   [<] [1] [>]   │
└────────────────────────────────────────────────────────┘
```

- Header: sticky, #F9FAFB background
- Rows: alternating #FFFFFF and #F9FAFB
- Sortable: click header to sort
- Selectable: checkbox column

---

## Badges

### Status Badges
```
[✓ Complete]  <- Green background
[⚠ Warning]   <- Yellow background
[✕ Error]     <- Red background
[ℹ Info]      <- Blue background
```

### Category Badges
```
[Kitchen] [Bathroom] [Garage]
```

- Rounded corners (full)
- Small padding (4px 8px)
- Small text (12px)

---

## Progress

### Progress Bar
```
┌────────────────────────────────────────────┐
│ ████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ 40%                                        │
└────────────────────────────────────────────┘
```

- Height: 8px
- Background: #E5E7EB
- Fill: #2563EB (or semantic color)

### Step Progress
```
[●]────────[●]────────[○]────────[○]
Step 1    Step 2    Step 3    Step 4
```

---

## Charts

### Bar Chart
```
     ┌────┐
     │    │  ┌────┐
┌────┤    │  │    │
│    │    │  │    │  ┌────┐
│    │    │  │    │  │    │
└────┴────┴──┴────┴──┴────┘
 Jan   Feb   Mar   Apr
```

### Donut Chart
```
      ┌───────┐
     ╱         ╲
    │    ┌──┐   │
     ╲   │45%│  ╱
      └──┴──┴──┘
       Plywood
```

---

## Design Tokens

| Component | Property | Value |
|-----------|----------|-------|
| Table header | Background | #F9FAFB |
| Table row alt | Background | #F9FAFB |
| Badge success | Background | #D1FAE5 |
| Badge warning | Background | #FEF3C7 |
| Badge error | Background | #FEE2E2 |
| Progress fill | Color | #2563EB |
