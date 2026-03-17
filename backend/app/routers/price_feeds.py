"""
Price Feeds Router - API endpoints for live supplier price comparison
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

from app.price_feeds import (
    PriceFeedManager,
    Supplier,
    get_supplier_search_links,
    get_estimated_price_range,
    get_all_price_estimates,
    compare_hardware_prices
)

router = APIRouter(prefix="/api/pricing", tags=["price-feeds"])


class SupplierEnum(str, Enum):
    ROCKLER = "rockler"
    WOODCRAFT = "woodcraft"
    HOME_DEPOT = "home_depot"
    LOWES = "lowes"
    MCMASTER = "mcmaster"
    AMAZON = "amazon"
    WOODWORKER_EXPRESS = "woodworker_express"
    DK_HARDWARE = "dk_hardware"


class PriceComparisonRequest(BaseModel):
    product_name: str
    sku: Optional[str] = None
    suppliers: Optional[List[SupplierEnum]] = None


class SearchLinksRequest(BaseModel):
    query: str


@router.get("/suppliers")
async def list_suppliers():
    """List all supported suppliers with their details."""
    return [
        {
            "id": "rockler",
            "name": "Rockler",
            "url": "https://www.rockler.com",
            "specialty": "Woodworking tools and hardware",
            "api_available": False,
            "scraping_allowed": True
        },
        {
            "id": "woodcraft",
            "name": "Woodcraft",
            "url": "https://www.woodcraft.com",
            "specialty": "Woodworking supplies",
            "api_available": False,
            "scraping_allowed": True
        },
        {
            "id": "home_depot",
            "name": "Home Depot",
            "url": "https://www.homedepot.com",
            "specialty": "General home improvement",
            "api_available": True,
            "scraping_allowed": False
        },
        {
            "id": "lowes",
            "name": "Lowes",
            "url": "https://www.lowes.com",
            "specialty": "General home improvement",
            "api_available": False,
            "scraping_allowed": False
        },
        {
            "id": "mcmaster",
            "name": "McMaster-Carr",
            "url": "https://www.mcmaster.com",
            "specialty": "Industrial hardware and fasteners",
            "api_available": False,
            "scraping_allowed": True
        },
        {
            "id": "amazon",
            "name": "Amazon",
            "url": "https://www.amazon.com",
            "specialty": "Everything",
            "api_available": True,
            "scraping_allowed": False
        },
        {
            "id": "woodworker_express",
            "name": "Woodworker Express",
            "url": "https://www.woodworkerexpress.com",
            "specialty": "Cabinet hardware",
            "api_available": False,
            "scraping_allowed": True
        },
        {
            "id": "dk_hardware",
            "name": "DK Hardware",
            "url": "https://www.dkhardware.com",
            "specialty": "Cabinet hardware and tools",
            "api_available": False,
            "scraping_allowed": True
        }
    ]


@router.post("/search-links")
async def get_search_links(request: SearchLinksRequest):
    """
    Get search links for a product across all suppliers.
    
    Use this when live pricing is not available.
    Returns direct search URLs for each supplier.
    """
    links = get_supplier_search_links(request.query)
    
    return {
        "query": request.query,
        "search_links": links,
        "usage_tip": "Click links to check current pricing on each supplier's website"
    }


@router.post("/compare")
async def compare_prices(request: PriceComparisonRequest):
    """
    Compare prices across multiple suppliers.
    
    Note: This feature requires supplier API integration.
    For now, it returns search links for manual price checking.
    """
    try:
        result = await compare_hardware_prices(
            product_name=request.product_name,
            sku=request.sku or ""
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Price comparison failed: {str(e)}")


@router.get("/estimates")
async def get_price_estimates():
    """
    Get estimated price ranges for common hardware categories.
    
    These are reference prices based on typical market values.
    Use for budgeting and planning purposes.
    """
    estimates = get_all_price_estimates()
    
    # Format for readability
    formatted = {}
    for category, subcategories in estimates.items():
        formatted[category] = {
            subcat: {"low": prices[0], "high": prices[1]}
            for subcat, prices in subcategories.items()
        }
    
    return {
        "note": "These are estimated price ranges for planning purposes. Actual prices may vary.",
        "estimates": formatted
    }


@router.get("/estimates/{hardware_type}")
async def get_hardware_type_estimates(hardware_type: str):
    """Get price estimates for a specific hardware category."""
    estimates = get_all_price_estimates()
    
    category = estimates.get(hardware_type.lower())
    if not category:
        raise HTTPException(
            status_code=404, 
            detail=f"Hardware type '{hardware_type}' not found. Available: {list(estimates.keys())}"
        )
    
    return {
        "hardware_type": hardware_type,
        "estimates": {
            subcat: {"low": prices[0], "high": prices[1]}
            for subcat, prices in category.items()
        }
    }


@router.get("/estimates/{hardware_type}/{subcategory}")
async def get_specific_estimate(hardware_type: str, subcategory: str):
    """Get price estimate for a specific hardware type and subcategory."""
    low, high = get_estimated_price_range(hardware_type, subcategory)
    
    if low == 0 and high == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Combination '{hardware_type}/{subcategory}' not found"
        )
    
    return {
        "hardware_type": hardware_type,
        "subcategory": subcategory,
        "low_price": low,
        "high_price": high,
        "average_price": round((low + high) / 2, 2)
    }


@router.get("/quick-links/{query}")
async def quick_search(query: str):
    """
    Quick search across all suppliers.
    Returns search links for the given query.
    """
    links = get_supplier_search_links(query)
    
    return {
        "query": query,
        "links": [
            {"supplier": name, "url": url}
            for name, url in links.items()
        ]
    }
