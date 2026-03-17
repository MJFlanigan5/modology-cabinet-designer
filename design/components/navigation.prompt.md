# Navigation Components

## Purpose
Core navigation system for KerfOS.

---

## Pencil Prompt

```
Design navigation components for KerfOS.

1. Top navigation bar:
   - Logo (left)
   - Search (center)
   - User menu (right)
   - Notification bell
   - Breadcrumbs

2. Sidebar navigation:
   - Collapsible sections
   - Active state highlighting
   - Icon + text items
   - Nested items
   - Collapse/expand toggle

3. Bottom navigation (mobile):
   - 4-5 items max
   - Icon + label
   - Active indicator
   - Safe area padding

4. Tabs:
   - Horizontal tabs
   - Pill tabs
   - Underline tabs
   - Vertical tabs (sidebar)

5. Breadcrumbs:
   - Home > Category > Item
   - Truncation for deep nesting
```

---

## Top Navigation

```
┌────────────────────────────────────────────────────────┐
│ [Logo]     [🔍 Search...]     [🔔] [👤 User ▾]          │
└────────────────────────────────────────────────────────┘
```

- Height: 64px
- Background: #FFFFFF
- Border bottom: 1px #E5E7EB
- Shadow: sm (optional)

---

## Sidebar Navigation

```
┌──────────────┐
│ 📁 Projects  │
│   └ Kitchen  │
│   └ Bathroom │
│ 📦 Templates │
│ 🔧 Hardware  │
│ ⚙️ Settings  │
└──────────────┘
```

- Width: 240px (collapsed: 64px)
- Background: #F9FAFB
- Active item: #DBEAFE background, #2563EB text
- Hover: #F3F4F6 background

---

## Bottom Navigation (Mobile)

```
┌────────────────────────────────────────────┐
│   🏠      📦      ➕      🔧      👤       │
│  Home  Projects  Add  Settings  Profile   │
└────────────────────────────────────────────┘
```

- Height: 64px + safe area
- Background: #FFFFFF
- Border top: 1px #E5E7EB
- Active: #2563EB icon and label

---

## Tabs

### Horizontal Tabs
```
┌─────────┬─────────┬─────────┐
│ Tab 1   │ Tab 2   │ Tab 3   │
│ ─────── │         │         │
└─────────┴─────────┴─────────┘
```

### Pill Tabs
```
┌─────────────────────────────────┐
│ [Tab 1]  Tab 2   Tab 3         │
└─────────────────────────────────┘
```

---

## Design Tokens

| Element | Property | Value |
|---------|----------|-------|
| Nav bar | Height | 64px |
| Sidebar | Width | 240px |
| Sidebar collapsed | Width | 64px |
| Bottom nav | Height | 64px |
| Active indicator | Color | #2563EB |
