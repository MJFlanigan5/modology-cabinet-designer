# Modology Cabinet Designer

AI-powered cabinet design tool that makes professional fabrication accessible to everyone.

## 🎯 Vision

Make professional cabinet fabrication accessible to DIYers and small shops by automating the complex parts: design optimization, cut list generation, and hardware sourcing.

## 🚀 Features

### Core Features (MVP)
- **Cabinet Builder UI** - Drag-and-drop cabinet components (boxes, doors, drawers, shelves)
- **3D Preview** - Real-time 3D visualization of cabinet designs
- **Material Library** - Pre-configured materials (plywood, MDF, hardwood) with dimensions
- **Cut List Generator** - Optimized 2D cutting plans for sheet goods
- **Hardware Finder** - Suggest hinges, slides, screws based on cabinet dimensions
- **Pricing Calculator** - Estimate material and hardware costs
- **Export Options** - PDF cut lists, CSV, DXF for CNC machines
- **User Accounts** - Save projects and return later

### Nice-to-Have (Phase 2)
- **Project Templates** - Pre-built cabinet designs (kitchen, vanity, bookshelf)
- **Waste Optimization** - Bin packing algorithm for sheet goods
- **CNC G-code Export** - Direct output for ShopBot, Shapeoko, etc.
- **Hardware Integration** - Direct links to suppliers (Rockler, Woodcraft, etc.)
- **Collaboration** - Share projects with others

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|---|---|
| **Next.js 14** | React framework with App Router |
| **React** | UI components |
| **Three.js** | 3D rendering and visualization |
| **Tailwind CSS** | Styling and responsive design |
| **Clerk** | User authentication |
| **Vercel** | Deployment (or Cloudflare Pages) |

### Backend
| Technology | Purpose |
|---|---|
| **FastAPI** | Python web framework |
| **SQLAlchemy** | ORM and database management |
| **PostgreSQL** | Database (via Railway) |
| **Pydantic** | Data validation |
| **Uvicorn** | ASGI server |
| **Railway** | Deployment and hosting |

## 📁 Project Structure

```
modology-cabinet-designer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py          # Database configuration
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── init_db.py           # Database initialization script
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── cabinets.py       # Cabinet CRUD endpoints
│   │       ├── materials.py      # Material management
│   │       └── hardware.py      # Hardware inventory
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt         # Python dependencies
│   └── main.py                 # Application entry point
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx       # Root layout with ClerkProvider
│   │   │   ├── page.tsx         # Home page
│   │   │   └── globals.css      # Global styles
│   │   └── lib/
│   │       └── api.ts           # API client
│   ├── package.json             # NPM dependencies
│   ├── tsconfig.json           # TypeScript config
│   ├── tailwind.config.ts       # Tailwind CSS config
│   └── next.config.mjs          # Next.js config
├── .github/
│   └── workflows/
│       ├── frontend.yml          # Frontend CI/CD (Cloudflare Pages)
│       ├── backend.yml           # Backend CI/CD (Railway)
│       └── rollback.yml          # Rollback workflow
├── README.md
└── LICENSE
```

## 🗄️ Database Setup

### 1. Create PostgreSQL Database on Railway

1. Go to your Railway project dashboard
2. Click **New Service** → **Database** → **PostgreSQL**
3. Wait for the database to deploy (30-60 seconds)
4. Click on the PostgreSQL service
5. Go to the **Variables** tab
6. Copy the `DATABASE_URL`
   
   **Example format:**
   ```
   postgresql://postgres:password@containers.us-west-1.railway.app:5432/railway
   ```

### 2. Add DATABASE_URL to Railway Backend

1. Go back to your FastAPI backend service
2. Go to the **Variables** tab
3. Add a new variable:
   - **Name:** `DATABASE_URL`
   - **Value:** Paste the DATABASE_URL you copied from the PostgreSQL service
   - **Or:** Use the "Reference" feature to link to the PostgreSQL service

### 3. Initialize Database Tables

**Option A: Automatic (Recommended)**

The database tables will be created automatically when the backend starts, thanks to the `lifespan` function in `main.py`.

**Option B: Manual Endpoint**

Visit: `https://your-backend.railway.app/init-db`

**Expected response:**
```json
{
  "status": "success",
  "message": "Database tables created/verified",
  "tables": [
    "cabinets",
    "materials",
    "hardware",
    "cabinet_components",
    "cut_lists",
    "cut_items",
    "projects",
    "project_cabinets"
  ]
}
```

### 4. Add Database URL to GitHub Secrets

For CI/CD pipelines:

1. Go to: https://github.com/MJFlanigan5/modology-cabinet-designer/settings/secrets/actions
2. Add secret:
   - **Name:** `RAILWAY_DATABASE_URL`
   - **Value:** Your DATABASE_URL from Railway

## 🔐 Environment Variables

### Backend (Railway)

| Variable | Description | How to Get |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | Auto-populated by Railway |
| `NEXT_PUBLIC_API_URL` | Your Railway backend URL | Railway dashboard |
| `NEXTAUTH_SECRET` | Random string for NextAuth | `openssl rand -base64 32` |
| `NEXTAUTH_URL` | Your Cloudflare Pages URL | Cloudflare Pages dashboard |
| `CLERK_PUBLISHABLE_KEY` | Clerk publishable key | Clerk Dashboard |
| `CLERK_SECRET_KEY` | Clerk secret key | Clerk Dashboard |
| `STRIPE_API_KEY` | Stripe API key | Stripe Dashboard |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook secret | Stripe Dashboard |

### Frontend (Cloudflare Pages)

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_URL` | Your Railway backend URL |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Clerk publishable key |

## 📊 Database Models

### Core Tables
| Table | Description |
|---|---|
| `cabinets` | Cabinet designs with dimensions and materials |
| `materials` | Sheet goods (plywood, MDF, hardwood) with pricing |
| `hardware` | Cabinet hardware (hinges, slides, handles) |
| `cabinet_components` | Individual parts of a cabinet |
| `cut_lists` | Optimized cutting plans for CNC/saw |
| `cut_items` | Individual cut positions on sheets |
| `projects` | Group cabinets into projects |

## 🚦 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL (local or Railway)
- Railway account
- GitHub account
- Cloudflare account (for Pages deployment)
- Clerk account (for authentication)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MJFlanigan5/modology-cabinet-designer.git
   cd modology-cabinet-designer
   ```

2. **Set up backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   export DATABASE_URL="postgresql://user:password@localhost:5432/cabinet_designer"
   python -m app.init_db
   uvicorn main:app --reload
   ```

3. **Set up frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Production Deployment

#### Frontend (Cloudflare Pages)
1. Connect GitHub repo to Cloudflare Pages
2. Configure build settings:
   - **Build command:** `cd frontend && npm run build`
   - **Build output directory:** `frontend/.next`
3. Set environment variables
4. Deploy automatically on push to `main`

#### Backend (Railway)
1. Connect GitHub repo to Railway
2. Configure:
   - **Root directory:** `backend`
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Add PostgreSQL database service
4. Add environment variables
5. Deploy automatically on push to `main`

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📝 API Endpoints

### Health
- `GET /` - API info
- `GET /health` - Health check
- `GET /init-db` - Initialize database tables

### Cabinets
- `POST /api/cabinets` - Create cabinet
- `GET /api/cabinets` - List all cabinets
- `GET /api/cabinets/{id}` - Get cabinet by ID
- `PUT /api/cabinets/{id}` - Update cabinet
- `DELETE /api/cabinets/{id}` - Delete cabinet

### Materials
- `POST /api/materials` - Create material
- `GET /api/materials` - List all materials
- `GET /api/materials/{id}` - Get material by ID
- `PUT /api/materials/{id}` - Update material
- `DELETE /api/materials/{id}` - Delete material

### Hardware
- `POST /api/hardware` - Create hardware
- `GET /api/hardware` - List all hardware
- `GET /api/hardware/{id}` - Get hardware by ID
- `DELETE /api/hardware/{id}` - Delete hardware

## 🔐 Security

- All endpoints use CORS configuration
- Database connections use environment variables
- Authentication via Clerk (frontend) and JWT (backend)
- Input validation via Pydantic
- SQL injection prevention via SQLAlchemy

## 📈 Roadmap

### Phase 1: MVP (Months 1-2)
- [x] Set up GitHub repository
- [x] Create database models and migrations
- [x] Implement basic CRUD endpoints
- [ ] Build cabinet builder UI
- [ ] Implement 2D cut list generator
- [ ] Add pricing calculator
- [ ] Deploy to Cloudflare Pages + Railway

### Phase 2: Advanced Features (Months 3-4)
- [ ] 3D preview with Three.js
- [ ] Waste optimization algorithm
- [ ] CNC G-code export
- [ ] Hardware finder with supplier integration
- [ ] User accounts and authentication
- [ ] Payment integration with Stripe

### Phase 3: Launch & Growth (Month 5+)
- [ ] Beta launch to 10 users
- [ ] Collect feedback and iterate
- [ ] Public launch
- [ ] Marketing and content creation
- [ ] Plan Phase 4 features

## 🤝 Contributing

This is currently a solo project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

**Michael Flanigan** - Modology Studios

## 🔗 Links

- [Modology Studios](https://www.modologystudios.com/)
- [GitHub Repository](https://github.com/MJFlanigan5/modology-cabinet-designer)

## 💬 Support

For questions or issues, please open a GitHub issue.