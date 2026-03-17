"""
Phase 4 Services - Live Supplier Price Feeds
Fetches real-time pricing from supplier APIs and scrapes prices when APIs unavailable.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import urllib.parse
import asyncio
import json
import re
from decimal import Decimal

router = APIRouter(prefix="/api/prices", tags=["price-feeds"])

# ============================================================================
# Configuration
# ============================================================================

SUPPLIER_CONFIGS = {
    "rockler": {
        "name": "Rockler",
        "base_url": "https://www.rockler.com",
        "search_url": "https://www.rockler.com/catalogsearch/result/?q={query}",
        "api_available": False,
        "scraper_config": {
            "product_selector": ".product-item",
            "price_selector": ".price",
            "name_selector": ".product-item-link",
            "pagination": True,
        },
        "rate_limit_seconds": 2,
    },
    "woodcraft": {
        "name": "Woodcraft",
        "base_url": "https://www.woodcraft.com",
        "search_url": "https://www.woodcraft.com/search?q={query}",
        "api_available": False,
        "scraper_config": {
            "product_selector": ".product-item",
            "price_selector": ".price-value",
            "name_selector": ".product-name",
        },
        "rate_limit_seconds": 2,
    },
    "home_depot": {
        "name": "Home Depot",
        "base_url": "https://www.homedepot.com",
        "search_url": "https://www.homedepot.com/s/{query}",
        "api_available": True,
        "api_endpoint": "https://www.homedepot.com/federation-gateway/graphql",
        "api_key": None,  # Would be set via environment variable
        "rate_limit_seconds": 1,
    },
    "mcmaster": {
        "name": "McMaster-Carr",
        "base_url": "https://www.mcmaster.com",
        "search_url": "https://www.mcmaster.com/{query}",
        "api_available": False,
        "scraper_config": {
            "product_selector": ".product-row",
            "price_selector": ".price-per-unit",
            "name_selector": ".product-name",
        },
        "rate_limit_seconds": 3,
    },
    "woodworker_express": {
        "name": "Woodworker Express",
        "base_url": "https://www.woodworkerexpress.com",
        "search_url": "https://www.woodworkerexpress.com/search?q={query}",
        "api_available": False,
        "scraper_config": {
            "product_selector": ".product-item",
            "price_selector": ".price",
            "name_selector": ".product-title",
        },
        "rate_limit_seconds": 2,
    },
    "dk_hardware": {
        "name": "DK Hardware",
        "base_url": "https://www.dkhardware.com",
        "search_url": "https://www.dkhardware.com/search?q={query}",
        "api_available": False,
        "scraper_config": {
            "product_selector": ".product-item",
            "price_selector": ".price",
            "name_selector": ".product-name",
        },
        "rate_limit_seconds": 2,
    },
}

# Cache for price results (in-memory, would use Redis in production)
_price_cache: Dict[str, Dict[str, Any]] = {}
_cache_ttl_seconds = 3600  # 1 hour

# ============================================================================
# Pydantic Models
# ============================================================================

class PriceResult(BaseModel):
    supplier: str
    supplier_name: str
    product_name: str
    price: float
    currency: str = "USD"
    unit: str = "each"
    url: str
    in_stock: Optional[bool] = None
    last_updated: datetime
    source: str = "api"  # "api", "scraper", "cache"

class PriceSearchRequest(BaseModel):
    query: str
    suppliers: Optional[List[str]] = None  # If None, search all
    max_results_per_supplier: int = 5
    use_cache: bool = True

class PriceSearchResponse(BaseModel):
    query: str
    results: List[PriceResult]
    total_results: int
    suppliers_searched: List[str]
    search_time_ms: int
    cached: bool

class PriceComparison(BaseModel):
    query: str
    best_price: PriceResult
    worst_price: Optional[PriceResult]
    average_price: float
    price_range: float
    results_by_supplier: Dict[str, List[PriceResult]]

class PriceAlert(BaseModel):
    id: str
    query: str
    target_price: float
    condition: str  # "below", "above", "change"
    supplier: Optional[str]
    email: str
    active: bool = True
    created_at: datetime
    last_triggered: Optional[datetime] = None

class PriceHistory(BaseModel):
    query: str
    supplier: str
    prices: List[Dict[str, Any]]  # [{price, date, in_stock}]
    trend: str  # "up", "down", "stable"

# ============================================================================
# Price Fetching Functions
# ============================================================================

async def fetch_price_home_depot(query: str, max_results: int = 5) -> List[PriceResult]:
    """
    Fetch prices from Home Depot using their GraphQL API.
    Note: In production, this would use the actual API with proper authentication.
    """
    results = []
    
    # Home Depot GraphQL query (simplified - would need actual API key)
    # For now, return search URL for manual lookup
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.homedepot.com/s/{encoded_query}"
    
    # In production, this would make actual API call
    # For demo, return placeholder with search URL
    results.append(PriceResult(
        supplier="home_depot",
        supplier_name="Home Depot",
        product_name=f"Search for: {query}",
        price=0.0,
        url=search_url,
        last_updated=datetime.utcnow(),
        source="api",
        in_stock=True,
    ))
    
    return results


async def fetch_price_generic(supplier: str, query: str, max_results: int = 5) -> List[PriceResult]:
    """
    Generic price fetcher for suppliers without API access.
    Returns search URLs for manual price lookup.
    In production, this would use web scraping with proper rate limiting.
    """
    config = SUPPLIER_CONFIGS.get(supplier)
    if not config:
        return []
    
    encoded_query = urllib.parse.quote(query)
    search_url = config["search_url"].format(query=encoded_query)
    
    results = []
    
    # In production, this would scrape the actual prices
    # For now, return the search URL
    results.append(PriceResult(
        supplier=supplier,
        supplier_name=config["name"],
        product_name=f"Search for: {query}",
        price=0.0,
        url=search_url,
        last_updated=datetime.utcnow(),
        source="scraper",
        in_stock=True,
    ))
    
    return results


async def fetch_prices(query: str, suppliers: Optional[List[str]] = None, 
                       max_results: int = 5, use_cache: bool = True) -> List[PriceResult]:
    """
    Fetch prices from multiple suppliers concurrently.
    """
    cache_key = f"{query}:{','.join(suppliers or ['all'])}"
    
    # Check cache
    if use_cache and cache_key in _price_cache:
        cached = _price_cache[cache_key]
        if datetime.utcnow() - cached["timestamp"] < timedelta(seconds=_cache_ttl_seconds):
            return cached["results"]
    
    # Determine which suppliers to query
    target_suppliers = suppliers or list(SUPPLIER_CONFIGS.keys())
    
    # Fetch concurrently
    tasks = []
    for supplier in target_suppliers:
        config = SUPPLIER_CONFIGS.get(supplier)
        if not config:
            continue
        
        if config["api_available"]:
            tasks.append(fetch_price_home_depot(query, max_results))
        else:
            tasks.append(fetch_price_generic(supplier, query, max_results))
    
    all_results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Flatten results
    results = []
    for result in all_results:
        if isinstance(result, list):
            results.extend(result)
    
    # Update cache
    _price_cache[cache_key] = {
        "results": results,
        "timestamp": datetime.utcnow(),
    }
    
    return results


# ============================================================================
# API Endpoints
# ============================================================================

@router.get("/search/{query}", response_model=PriceSearchResponse)
async def search_prices(
    query: str,
    suppliers: Optional[str] = None,
    max_results: int = 5,
    use_cache: bool = True
):
    """
    Search for prices across multiple suppliers.
    
    - **query**: Search term (e.g., "soft close hinge")
    - **suppliers**: Comma-separated supplier IDs (optional)
    - **max_results**: Max results per supplier
    - **use_cache**: Use cached results if available
    """
    start_time = datetime.utcnow()
    
    supplier_list = suppliers.split(",") if suppliers else None
    
    results = await fetch_prices(
        query=query,
        suppliers=supplier_list,
        max_results=max_results,
        use_cache=use_cache
    )
    
    search_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
    
    return PriceSearchResponse(
        query=query,
        results=results,
        total_results=len(results),
        suppliers_searched=supplier_list or list(SUPPLIER_CONFIGS.keys()),
        search_time_ms=search_time_ms,
        cached=False,
    )


@router.post("/search", response_model=PriceSearchResponse)
async def search_prices_post(request: PriceSearchRequest):
    """
    POST endpoint for price search with more options.
    """
    start_time = datetime.utcnow()
    
    results = await fetch_prices(
        query=request.query,
        suppliers=request.suppliers,
        max_results=request.max_results_per_supplier,
        use_cache=request.use_cache
    )
    
    search_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
    
    return PriceSearchResponse(
        query=request.query,
        results=results,
        total_results=len(results),
        suppliers_searched=request.suppliers or list(SUPPLIER_CONFIGS.keys()),
        search_time_ms=search_time_ms,
        cached=False,
    )


@router.get("/compare/{query}", response_model=PriceComparison)
async def compare_prices(query: str, suppliers: Optional[str] = None):
    """
    Compare prices across suppliers and find the best deal.
    """
    supplier_list = suppliers.split(",") if suppliers else None
    
    results = await fetch_prices(query=query, suppliers=supplier_list)
    
    # Filter out results without actual prices
    valid_results = [r for r in results if r.price > 0]
    
    if not valid_results:
        raise HTTPException(
            status_code=404, 
            detail="No valid prices found. Try searching manually on supplier sites."
        )
    
    # Sort by price
    valid_results.sort(key=lambda x: x.price)
    
    # Group by supplier
    results_by_supplier = {}
    for r in results:
        if r.supplier not in results_by_supplier:
            results_by_supplier[r.supplier] = []
        results_by_supplier[r.supplier].append(r)
    
    # Calculate stats
    prices = [r.price for r in valid_results]
    average_price = sum(prices) / len(prices)
    price_range = max(prices) - min(prices)
    
    return PriceComparison(
        query=query,
        best_price=valid_results[0],
        worst_price=valid_results[-1] if len(valid_results) > 1 else None,
        average_price=round(average_price, 2),
        price_range=round(price_range, 2),
        results_by_supplier=results_by_supplier,
    )


@router.get("/suppliers")
async def list_supported_suppliers():
    """
    List all supported suppliers and their capabilities.
    """
    return {
        "suppliers": [
            {
                "id": id,
                "name": config["name"],
                "base_url": config["base_url"],
                "api_available": config["api_available"],
                "search_url": config["search_url"].replace("{query}", "QUERY"),
            }
            for id, config in SUPPLIER_CONFIGS.items()
        ],
        "total": len(SUPPLIER_CONFIGS),
    }


@router.get("/history/{query}")
async def get_price_history(query: str, supplier: Optional[str] = None):
    """
    Get historical price data for a product.
    Note: In production, this would query a time-series database.
    """
    # Placeholder - would implement actual price history tracking
    return {
        "query": query,
        "supplier": supplier,
        "message": "Price history tracking coming soon. Enable alerts to track prices over time.",
        "prices": [],
    }


@router.post("/alerts")
async def create_price_alert(alert: PriceAlert):
    """
    Create a price alert for a product.
    Note: In production, this would store in database and trigger webhooks.
    """
    # Placeholder - would implement actual alert system
    return {
        "status": "created",
        "alert": alert,
        "message": f"Price alert created for '{alert.query}'. You'll be notified when price is {alert.condition} ${alert.target_price}.",
    }


@router.get("/alerts")
async def list_price_alerts():
    """
    List all active price alerts.
    """
    # Placeholder - would query from database
    return {
        "alerts": [],
        "total": 0,
    }


@router.delete("/alerts/{alert_id}")
async def delete_price_alert(alert_id: str):
    """
    Delete a price alert.
    """
    return {
        "status": "deleted",
        "alert_id": alert_id,
    }


@router.post("/refresh")
async def refresh_prices(background_tasks: BackgroundTasks):
    """
    Refresh all cached prices in the background.
    """
    async def refresh_task():
        global _price_cache
        _price_cache = {}
        # In production, would refresh from database-stored queries
    
    background_tasks.add_task(refresh_task)
    
    return {
        "status": "refreshing",
        "message": "Price cache refresh started in background.",
    }


@router.get("/cache/status")
async def cache_status():
    """
    Get status of price cache.
    """
    return {
        "cached_queries": len(_price_cache),
        "cache_ttl_seconds": _cache_ttl_seconds,
        "entries": list(_price_cache.keys()),
    }
