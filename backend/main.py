from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Dict, Any

from app.routers import cabinets, materials, hardware, cutlists
from app.database import engine, get_db
from app.models import Base
from app.gcode_generator import generate_gcode, GCodeConfig

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Modology Cabinet Designer API",
    description="API for AI-powered cabinet design tool",
    version="0.1.0",
    lifespan=lifespan
)

# CORS - Allow Vercel, Fly.io, and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:4173",
        "https://modologystudios.com",
        "*.pages.dev",  # Cloudflare Pages preview URLs
        "*.onrender.com",  # Render backend
        "*.fly.dev"  # Fly.io backend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Modology Cabinet Designer API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/init-db")
async def init_database():
    """
    Initialize database tables.
    This endpoint can be used to manually trigger table creation.
    """
    try:
        Base.metadata.create_all(bind=engine)
        tables = list(Base.metadata.tables.keys())
        return {
            "status": "success",
            "message": "Database tables created/verified",
            "tables": tables
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# G-code generation endpoint
class GCodeRequest(BaseModel):
    """Request model for G-code generation"""
    cutList: Dict[str, Any]  # Cut list from cutlists router

@app.post("/api/gcode")
async def generate_gcode_endpoint(request: GCodeRequest):
    """
    Generate G-code from cut list data
    """
    try:
        # Generate G-code using the generator
        gcode_content = generate_gcode(request.cutList)
        
        # Generate metadata
        total_sheets = len(request.cutList.get("cutList", []))
        total_cuts = sum(len(sheet.get("cuts", [])) for sheet in request.cutList.get("cutList", []))
        
        metadata = {
            "gcode": gcode_content,
            "metadata": {
                "totalSheets": total_sheets,
                "totalCuts": total_cuts,
                "estimatedTime": total_cuts * 2,  # ~2 min per operation
                "materialThickness": 18.0  # mm (3/4" plywood)
            }
        }
        
        return metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate G-code: {str(e)}")

# Include routers
app.include_router(cabinets.router)
app.include_router(materials.router)
app.include_router(hardware.router)
app.include_router(cutlists.router)
