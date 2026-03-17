"""
Localization Router - Local Supplier Search API
Find suppliers near a zip code with pricing and availability
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..localization import (
    find_local_suppliers,
    get_supplier_search_links,
    compare_local_prices,
    get_local_inventory_status,
    SupplierCategory,
    StoreType,
)

router = APIRouter(prefix="/api/localization", tags=["localization"])


@router.get("/suppliers/{zip_code}")
async def search_local_suppliers(
    zip_code: str,
    radius: float = Query(25.0, description="Search radius in miles"),
    categories: Optional[str] = Query(None, description="Comma-separated categories"),
    store_types: Optional[str] = Query(None, description="Comma-separated store types"),
    max_results: int = Query(20, description="Maximum number of results"),
):
    """
    Find local suppliers near a zip code.
    
    - **zip_code**: US zip code (5 digits)
    - **radius**: Search radius in miles (default: 25)
    - **categories**: Filter by categories (plywood, hardware, tools, finishes, hardwood, fasteners, edge_banding)
    - **store_types**: Filter by store types (big_box, hardware_chain, specialty_woodworking, lumber_yard, online)
    """
    
    # Validate zip code
    if not zip_code or len(zip_code) < 5:
        raise HTTPException(status_code=400, detail="Invalid zip code")
    
    # Parse categories
    category_list = None
    if categories:
        try:
            category_list = [SupplierCategory(c.strip()) for c in categories.split(",")]
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid category: {e}")
    
    # Parse store types
    store_type_list = None
    if store_types:
        try:
            store_type_list = [StoreType(t.strip()) for t in store_types.split(",")]
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid store type: {e}")
    
    result = find_local_suppliers(
        zip_code=zip_code[:5],
        radius_miles=radius,
        categories=category_list,
        store_types=store_type_list,
        max_results=max_results,
    )
    
    return {
        "zip_code": result.zip_code,
        "coordinates": result.coordinates,
        "suppliers": [
            {
                "id": s.supplier_id,
                "supplier_key": s.supplier_key,
                "name": s.name,
                "type": s.type.value,
                "distance_miles": s.distance_miles,
                "address": s.address,
                "phone": s.phone,
                "lat": s.lat,
                "lng": s.lng,
                "categories": [c.value for c in s.categories],
                "price_tier": s.price_tier,
                "store_url": s.store_url,
                "search_url": s.search_url,
                "in_stock_probability": s.in_stock_probability,
            }
            for s in result.suppliers
        ],
        "total_count": result.total_count,
        "by_type": result.by_type,
        "recommendations": result.recommendations,
    }


@router.get("/price-comparison/{zip_code}")
async def price_comparison(
    zip_code: str,
    item: str = Query(..., description="Item to compare prices for"),
    category: Optional[str] = Query(None, description="Item category"),
):
    """
    Compare prices for an item across local and online suppliers.
    
    - **zip_code**: US zip code
    - **item**: Item name to search for
    - **category**: Optional category filter
    """
    
    cat = None
    if category:
        try:
            cat = SupplierCategory(category)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    
    result = compare_local_prices(
        zip_code=zip_code[:5],
        item_name=item,
        category=cat,
    )
    
    return result


@router.get("/search-links")
async def get_search_links(
    search_terms: str = Query(..., description="Comma-separated search terms"),
    suppliers: Optional[str] = Query(None, description="Comma-separated supplier keys"),
):
    """
    Generate direct search links for suppliers.
    
    - **search_terms**: Items to search for (comma-separated)
    - **suppliers**: Optional specific suppliers to include
    """
    
    terms = [t.strip() for t in search_terms.split(",")]
    supplier_list = [s.strip() for s in suppliers.split(",")] if suppliers else None
    
    return get_supplier_search_links(
        zip_code="",  # Not needed for this endpoint
        search_terms=terms,
        suppliers=supplier_list,
    )


@router.get("/inventory/{zip_code}/{supplier_key}")
async def check_inventory(
    zip_code: str,
    supplier_key: str,
    item: str = Query(..., description="Item to check"),
):
    """
    Check local inventory status for an item.
    
    - **zip_code**: US zip code
    - **supplier_key**: Supplier identifier (e.g., home_depot, lowes)
    - **item**: Item name to check
    """
    
    return get_local_inventory_status(
        zip_code=zip_code[:5],
        item_name=item,
        supplier_key=supplier_key,
    )


@router.get("/categories")
async def list_categories():
    """List all available supplier categories."""
    return {
        "categories": [
            {"value": c.value, "label": c.value.replace("_", " ").title()}
            for c in SupplierCategory
        ]
    }


@router.get("/store-types")
async def list_store_types():
    """List all available store types."""
    return {
        "store_types": [
            {"value": t.value, "label": t.value.replace("_", " ").title()}
            for t in StoreType
        ]
    }
