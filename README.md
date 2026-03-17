# Modology Cabinet Designer

AI-powered cabinet design tool that makes professional fabrication accessible to everyone.

## 🎯 Vision

Make professional cabinet fabrication accessible to DIYers and small shops by automating complex parts: design optimization, cut list generation, and hardware sourcing.

## 🚀 Features

### Core Features (MVP)

**Cabinet Builder UI** - Drag-and-drop cabinet components (boxes, doors, drawers, shelves)

**3D Preview** - Real-time 3D visualization of cabinet designs

**Material Library** - Pre-configured materials (plywood, MDF, hardwood) with dimensions

**Cut List Generator** - Optimized 2D cutting plans for sheet goods

**Hardware Finder** - Suggest hinges, slides, screws based on cabinet dimensions

**Pricing Calculator** - Estimate material and hardware costs

**Export Options** - PDF cut lists, CSV, DXF for CNC machines

**User Accounts** - Save projects and return later

### Nice-to-Have (Phase 2)

**Project Templates** - Pre-built cabinet designs (kitchen, vanity, bookshelf)

**Waste Optimization** - Bin packing algorithm for sheet goods

**CNC G-code Export** - Direct output for ShopBot, Shapeoko, etc.

**Hardware Integration** - Direct links to suppliers (Rockler, Woodcraft, Home Depot)

**Collaboration** - Share projects with others

## 🛠️ Tech Stack

### Frontend

| Technology | Purpose |
|---|---|
| **Next.js 14** | React framework with App Router |
| **React** | UI components |
| **Three.js** | 3D rendering and visualization |
| **Tailwind CSS** | Styling and responsive design |
| **Clerk** | User authentication |
| **Vercel** | Deployment |

### Backend

| Technology | Purpose |
|---|---|
| **FastAPI** | Python web framework |
| **SQLAlchemy** | ORM and database management |
| **PostgreSQL** | Database (via Fly.io) |
| **Pydantic** | Data validation |
| **Uvicorn** | ASGI server |
| **Fly.io** | Deployment and hosting |

## 📁 Project Structure

```
modology-cabinet-designer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py          # Database configuration
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── init_db.py           # Database initialization script
│   │   ├── gcode_generator.py   # G-code generation for CNC
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── cabinets.py       # Cabinet CRUD endpoints
│   │       ├── materials.py      # Material management
│   │       ├── hardware.py      # Hardware inventory with filtering
│   │       └── cutlists.py      # Cut list generation
│   ├── main.py                 # FastAPI application with G-code endpoint
│   ├── requirements.txt         # Python dependencies
│   ├── fly.toml                # Fly.io deployment config
│   └── Dockerfile              # Docker configuration
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx       # Root layout with ClerkProvider
│   │   │   ├── page.tsx         # Home page
│   │   │   └── globals.css      # Global styles
│   │   └── components/
│   │       ├── CabinetBuilder.tsx   # Main UI with 3D preview
│   │       ├── CabinetPreview.tsx   # Three.js 3D visualization
│   │       ├── MaterialSelector.tsx  # Material selection with pricing
│   │       ├── CabinetForm.tsx     # Add cabinets with presets
│   │       ├── DimensionEditor.tsx  # Component management
│   │       ├── CutListExporter.tsx  # PDF, CSV, DXF, G-code exports
│   │       ├── HardwareFinder.tsx   # Hardware browsing and selection
│   │       └── GCodeExporter.tsx   # G-code export functionality
│   ├── package.json             # NPM dependencies
│   ├── tsconfig.json           # TypeScript config
│   ├── tailwind.config.ts       # Tailwind CSS config
│   └── next.config.mjs          # Next.js config
├── .github/
│   └── workflows/
│       ├── frontend.yml          # Frontend CI/CD (Vercel)
│       ├── backend.yml           # Backend CI/CD (Fly.io)
│       └── rollback.yml          # Rollback workflow
├── README.md
└── LICENSE
```

## 🗄️ Database Setup

### 1. Create PostgreSQL Database on Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login to Fly.io
flyctl auth login

# Create PostgreSQL database
flyctl postgres create
```

### 2. Get Database Connection URL

```bash
flyctl postgres connect -a modology-db --console
```

Or to get connection URL:

```bash
flyctl status -a modology-db
```

You'll see something like:
```
Host: xxx-a.db.fly.dev
User: postgres
Database: modology_db
```

**Format your DATABASE_URL:**
```
postgresql://postgres:password@xxx-a.db.fly.dev:5432/modology_db
```

### 3. Attach Database to Backend App

```bash
flyctl postgres attach -a modology-backend modology-db
```

This will:
- Automatically set `DATABASE_URL` environment variable
- Configure firewall rules
- Connect backend to database securely

### 4. Update Secrets (if needed)

```bash
flyctl secrets set DATABASE_URL="postgresql://postgres:password@xxx-a.db.fly.dev:5432/modology_db"
```

## 🔐 Environment Variables

### Backend (Fly.io)

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string (auto-set by Fly.io) |
| `PORT` | 8000 (set by Fly.io automatically) |

### Frontend (Vercel)

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_URL` | Your Fly.io backend URL (e.g., `https://modology-backend.fly.dev`) |
| `NEXTAUTH_SECRET` | Random string for NextAuth (generate with `openssl rand -base64 32`) |
| `NEXTAUTH_URL` | Your Vercel frontend URL |
| `CLERK_PUBLISHABLE_KEY` | Clerk publishable key (from Clerk Dashboard) |
| `CLERK_SECRET_KEY` | Clerk secret key (from Clerk Dashboard) |

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

## 🦟 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL (local or Fly.io)
- GitHub account
- Vercel account
- Clerk account (for authentication)

### Local Development

#### 1. Clone the Repository

```bash
git clone https://github.com/MJFlanigan5/modology-cabinet-designer.git
cd modology-cabinet-designer
```

#### 2. Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set DATABASE_URL
export DATABASE_URL="postgresql://postgres:password@localhost:5432/modology_db"

# Initialize database
python -m app.init_db

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
cp .env.example .env.local
# Edit .env.local and add your API URL
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

#### 4. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Production Deployment

#### Deploy Backend to Fly.io

**Option A: Using Fly.io CLI (Recommended)**

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Deploy
cd backend
flyctl deploy
```

**Option B: Automatic Deployment via GitHub Actions**

The backend is automatically deployed when you push to the `main` branch via the `.github/workflows/backend.yml` workflow.

#### Deploy Frontend to Vercel

**Option A: Using Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel
```

**Option B: Automatic Deployment via GitHub Actions**

The frontend is automatically deployed when you push to the `main` branch via the `.github/workflows/frontend.yml` workflow.

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
- `GET /api/hardware?type={type}` - List hardware (optionally filtered by type)
- `GET /api/hardware/{id}` - Get hardware by ID
- `DELETE /api/hardware/{id}` - Delete hardware

### Cut Lists
- `POST /api/cutlists/generate` - Generate optimized cut list
- `GET /api/cutlists` - Get cut list history
- `GET /api/cutlists/{id}` - Get specific cut list
- `DELETE /api/cutlists/{id}` - Delete cut list

### G-code
- `POST /api/gcode` - Generate G-code from cut list

## 🔐 GitHub Secrets

### Backend (Fly.io)

| Secret | Description | How to Get It |
|---|---|---|
| `FLY_API_TOKEN` | Fly.io API token | https://fly.io/user/settings/tokens |
| `FLY_APP_NAME` | Fly.io app name | From `fly.toml` or CLI |

### Frontend (Vercel)

| Secret | Description | How to Get It |
|---|---|---|
| `VERCEL_TOKEN` | Vercel API token | https://vercel.com/account/tokens |
| `VERCEL_ORG_ID` | Vercel organization ID | From Vercel dashboard |

### Shared

| Secret | Description | How to Get It |
|---|---|---|
| `SLACK_WEBHOOK_URL` | Slack webhook for notifications | Create Slack app & add incoming webhook |

## 🎨 Deployment Architecture

```
┌─────────────────────────────────────────┐
│   Vercel (Frontend - Next.js)         │
│   - Cabinet Builder UI                 │
│   - Hardware Finder                   │
│   - 3D Preview                      │
│   - Cut List Exporter (PDF/CSV/DXF/G-code)│
└──────────────┬──────────────────────┘
               │
               │ API calls (same domain)
               ▼
┌─────────────────────────────────────────┐
│   Fly.io (Backend - FastAPI)           │
│   - FastAPI native support            │
│   - Cabinets, Materials, Hardware APIs  │
│   - Cut List Optimizer               │
│   - G-Code Generator                │
└──────────────┬──────────────────────┘
               │
               │ DATABASE_URL (same VPC)
               ▼
┌─────────────────────────────────────────┐
│   Fly.io PostgreSQL                   │
│   - Managed database                │
│   - Free tier included              │
│   - Same platform as backend          │
└─────────────────────────────────────────┘
```

## 🧹 Cleanup Required

### Files to Delete Manually

The following files were created during development but are no longer needed:

| File | Reason for Deletion |
|---|---|
| `render.yaml` | Not using Render anymore (using Fly.io) |
| `setup-railway.sh` | Not using Railway anymore (using Fly.io) |
| `setup-render.sh` | Not using Render anymore (using Fly.io) |
| `setup-fly.sh` | You had issues with this script, using manual deployment |

### How to Delete

**Option 1: Using Git Commands**

```bash
cd modology-cabinet-designer
git rm render.yaml setup-railway.sh setup-render.sh setup-fly.sh
git commit -m "Remove unused deployment files"
git push
```

**Option 2: Using GitHub Web UI**

1. Go to your repository on GitHub
2. Navigate to each file
3. Click the "..." (three dots) menu
4. Select "Delete file"
5. Repeat for all files listed above

## 🔐 Security

- All endpoints use CORS configuration
- Database connections use environment variables
- Input validation via Pydantic
- SQL injection prevention via SQLAlchemy
- G-code generation uses safe defaults

## 📈 Roadmap

### Phase 1: MVP (Months 1-2)
- [x] Set up GitHub repository
- [x] Create database models and migrations
- [x] Implement basic CRUD endpoints
- [x] Build cabinet builder UI
- [x] Implement 2D cut list generator
- [x] Add pricing calculator
- [ ] Deploy to Vercel (frontend)
- [ ] Deploy to Fly.io (backend)

### Phase 2: Advanced Features (Months 3-4)
- [x] 3D preview with Three.js
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
