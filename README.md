# Modology Cabinet Designer

AI-powered cabinet design tool with cut list generation and hardware sourcing.

## Vision

Make professional cabinet fabrication accessible to DIYers and small shops by automating the complex parts: design optimization, cut list generation, and hardware sourcing.

## Stack

- **Frontend**: Next.js 14 + React + Three.js + Tailwind CSS
- **Backend**: Python + FastAPI
- **Database**: PostgreSQL
- **Auth**: Clerk
- **Payment**: Stripe
- **Deployment**: Vercel (frontend) + Railway (backend)

## Features

### MVP (Phase 1)
- [ ] Cabinet Builder UI (drag-and-drop components)
- [ ] 3D Preview (Three.js)
- [ ] Material Library (plywood, MDF, hardwood)
- [ ] Cut List Generator (optimized 2D cutting plans)
- [ ] Hardware Finder (suggests hinges, slides, screws)
- [ ] Pricing Calculator (estimate material and hardware costs)
- [ ] Export Options (PDF cut list, CSV, DXF)
- [ ] User Accounts (save projects, return later)

### Phase 2 (Post-MVP)
- [ ] Project Templates (kitchen, vanity, bookshelf)
- [ ] Waste Optimization (bin packing algorithm)
- [ ] CNC G-code Export
- [ ] Hardware Integration (direct links to suppliers)
- [ ] Collaboration (share projects)

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL
- Clerk account (for auth)
- Stripe account (for payments)

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Roadmap

- **Weeks 1-4**: Foundation (project setup, cabinet components, cut list gen)
- **Weeks 5-8**: Core MVP (3D preview, hardware finder, exports, user accounts)
- **Weeks 9-12**: Polish & Revenue (Stripe, pricing page, templates)
- **Week 13+**: Launch & Iterate

## License

MIT © 2026 Modology Studios