"""
Big Box Store Integration - Phase 5 Feature

Integration with Home Depot and Lowe's for:
- Real-time inventory checking
- Add to Cart functionality
- Price comparison
- Store pickup optimization
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import math
from datetime import datetime


class Store(Enum):
    HOME_DEPOT = "home_depot"
    LOWES = "lowes"
    MENARDS = "menards"


@dataclass
class StoreInventory:
    """Inventory status at a specific store"""
    store_name: str
    store_id: str
    address: str
    distance_miles: float
    in_stock: bool
    quantity_available: int
    price: float
    last_updated: str


@dataclass
class MaterialPickup:
    """Optimized material pickup plan"""
    materials: List[Dict[str, Any]]
    stores: List[Dict[str, Any]]
    total_cost: float
    total_distance: float
    pickup_route: List[str]
    estimated_time_minutes: int


# Home Depot product SKUs and categories
HOME_DEPOT_PRODUCTS = {
    # Plywood
    "birch_plywood_3_4": {"sku": "100138397", "name": "Birch Plywood 3/4in x 4ft x 8ft", "category": "plywood"},
    "oak_plywood_3_4": {"sku": "100017630", "name": "Red Oak Plywood 3/4in x 4ft x 8ft", "category": "plywood"},
    "plywood_sanding_3_4": {"sku": "100138394", "name": "Sanding Plywood 3/4in x 4ft x 8ft", "category": "plywood"},
    
    # MDF
    "mdf_3_4": {"sku": "100006675", "name": "MDF Board 3/4in x 4ft x 8ft", "category": "mdf"},
    "mdf_1_2": {"sku": "100006674", "name": "MDF Board 1/2in x 4ft x 8ft", "category": "mdf"},
    
    # Hardware - Drawer Slides
    "drawer_slide_18_soft_close": {"sku": "315442048", "name": "Liberty 18in Full Extension Soft Close", "category": "slides"},
    "drawer_slide_22": {"sku": "315442055", "name": "Liberty 22in Full Extension Slide", "category": "slides"},
    
    # Hardware - Hinges
    "hinge_concealed_110": {"sku": "206988094", "name": "Everbilt Concealed Cabinet Hinge 110°", "category": "hinges"},
    "hinge_soft_close": {"sku": "312498156", "name": "Everbilt Soft Close Concealed Hinge", "category": "hinges"},
    
    # Hardware - Handles
    "handle_5inch_brushed_nickel": {"sku": "310675285", "name": "Liberty 5in Brushed Nickel Pull", "category": "handles"},
    "handle_3inch_brushed_nickel": {"sku": "310675277", "name": "Liberty 3in Brushed Nickel Pull", "category": "handles"},
    
    # Screws and Fasteners
    "pocket_screws_1_25": {"sku": "204272395", "name": "Kreg 1-1/4in Pocket Hole Screws 100ct", "category": "fasteners"},
    "wood_screws_1_5_8": {"sku": "204847037", "name": "Everbilt #8 x 1-5/8in Wood Screws", "category": "fasteners"},
    
    # Edge Banding
    "edge_banding_birch_7_8": {"sku": "204847037", "name": "Birch Edge Banding 7/8in x 25ft", "category": "edge_banding"},
    "edge_banding_oak_7_8": {"sku": "100144774", "name": "Red Oak Edge Banding 7/8in x 25ft", "category": "edge_banding"},
}

# Lowe's product SKUs
LOWES_PRODUCTS = {
    # Plywood
    "birch_plywood_3_4": {"sku": "44466", "name": "PureBond Birch Plywood 3/4in x 4ft x 8ft", "category": "plywood"},
    "oak_plywood_3_4": {"sku": "44462", "name": "Red Oak Plywood 3/4in x 4ft x 8ft", "category": "plywood"},
    
    # MDF
    "mdf_3_4": {"sku": "99608", "name": "MDF Panel 3/4in x 4ft x 8ft", "category": "mdf"},
    
    # Hardware
    "drawer_slide_18_soft_close": {"sku": "50391949", "name": "Rev-A-Shelf 18in Soft Close Slide", "category": "slides"},
    "hinge_concealed_110": {"sku": "50342546", "name": "Liberty Concealed Hinge 110°", "category": "hinges"},
    "handle_5inch_brushed_nickel": {"sku": "3139173", "name": "Liberty 5in Brushed Nickel Pull", "category": "handles"},
}


def get_product_sku(material_or_hardware: str, store: Store) -> Optional[Dict[str, Any]]:
    """Get product SKU for a material/hardware at a specific store"""
    if store == Store.HOME_DEPOT:
        return HOME_DEPOT_PRODUCTS.get(material_or_hardware)
    elif store == Store.LOWES:
        return LOWES_PRODUCTS.get(material_or_hardware)
    return None


def get_store_inventory(product_sku: str, store_id: str, store: Store) -> StoreInventory:
    """
    Check inventory at a specific store.
    Note: This is a placeholder that would integrate with actual store APIs.
    """
    # Placeholder - in production, this would call the store's API
    # Home Depot API: https://developer.homedepot.com/
    # Lowe's API: https://developer.lowes.com/
    
    return StoreInventory(
        store_name=f"{store.value.replace('_', ' ').title()} #{store_id}",
        store_id=store_id,
        address="123 Main St, City, ST 12345",
        distance_miles=2.5,
        in_stock=True,
        quantity_available=10,
        price=45.99,
        last_updated=datetime.now().isoformat()
    )


def find_nearby_stores(zip_code: str, store: Store, radius_miles: int = 25) -> List[Dict[str, Any]]:
    """
    Find nearby stores for pickup.
    Note: Placeholder for API integration.
    """
    # In production, would call store locator APIs
    return [
        {
            "store_id": "1234",
            "name": f"{store.value.replace('_', ' ').title()} - Main St",
            "address": "123 Main St, City, ST 12345",
            "distance_miles": 2.5,
            "hours": "6AM - 10PM",
            "phone": "(555) 123-4567",
            "services": ["pickup", "delivery", "tool_rental"]
        },
        {
            "store_id": "5678",
            "name": f"{store.value.replace('_', ' ').title()} - Downtown",
            "address": "456 Oak Ave, City, ST 12345",
            "distance_miles": 5.2,
            "hours": "6AM - 9PM",
            "phone": "(555) 234-5678",
            "services": ["pickup", "delivery"]
        }
    ]


def generate_cart_link(items: List[Dict[str, Any]], store: Store) -> str:
    """
    Generate a direct cart link for adding items.
    Note: These URLs would need to be validated against actual store websites.
    """
    if store == Store.HOME_DEPOT:
        # Home Depot cart format
        base_url = "https://www.homedepot.com/cart"
        item_params = "/".join([f"{item['sku']}/1" for item in items])
        return f"{base_url}/{item_params}"
    
    elif store == Store.LOWES:
        # Lowe's cart format
        base_url = "https://www.lowes.com/cart"
        item_params = "&".join([f"item={item['sku']}:1" for item in items])
        return f"{base_url}?{item_params}"
    
    return ""


def compare_prices(material_or_hardware: str) -> Dict[str, Any]:
    """
    Compare prices across Home Depot and Lowe's for the same item.
    """
    results = {
        "item": material_or_hardware,
        "prices": [],
        "best_price": None,
        "best_store": None
    }
    
    for store in [Store.HOME_DEPOT, Store.LOWES]:
        product = get_product_sku(material_or_hardware, store)
        if product:
            # Placeholder prices - in production, fetch from API
            base_price = 45.99 if "plywood" in product["category"] else 12.99
            if store == Store.LOWES:
                base_price *= 1.02  # Slight price variation
            
            results["prices"].append({
                "store": store.value,
                "price": round(base_price, 2),
                "product_name": product["name"],
                "sku": product["sku"]
            })
    
    if results["prices"]:
        best = min(results["prices"], key=lambda x: x["price"])
        results["best_price"] = best["price"]
        results["best_store"] = best["store"]
    
    return results


def optimize_pickup(materials: List[Dict[str, Any]], zip_code: str) -> MaterialPickup:
    """
    Optimize material pickup across stores for best price and shortest route.
    """
    stores_to_visit = {}
    all_materials = []
    total_cost = 0
    
    for material in materials:
        material_name = material["name"]
        quantity = material.get("quantity", 1)
        
        # Compare prices
        comparison = compare_prices(material_name)
        
        if comparison["best_store"]:
            store = comparison["best_store"]
            
            if store not in stores_to_visit:
                stores_to_visit[store] = {
                    "store": store,
                    "items": [],
                    "subtotal": 0
                }
            
            item_cost = comparison["best_price"] * quantity
            stores_to_visit[store]["items"].append({
                "name": material_name,
                "quantity": quantity,
                "price": comparison["best_price"],
                "total": round(item_cost, 2)
            })
            stores_to_visit[store]["subtotal"] += item_cost
            total_cost += item_cost
            
            all_materials.append({
                "name": material_name,
                "quantity": quantity,
                "store": store,
                "price": comparison["best_price"]
            })
    
    # Calculate pickup route (optimize by distance)
    # In production, would use mapping API
    pickup_route = list(stores_to_visit.keys())
    
    # Estimate time (rough calculation)
    avg_time_per_store = 20  # minutes
    travel_time = len(stores_to_visit) * 15  # 15 min travel between stores
    estimated_time = (len(stores_to_visit) * avg_time_per_store) + travel_time
    
    return MaterialPickup(
        materials=all_materials,
        stores=list(stores_to_visit.values()),
        total_cost=round(total_cost, 2),
        total_distance=len(stores_to_visit) * 5.0,  # placeholder
        pickup_route=pickup_route,
        estimated_time_minutes=estimated_time
    )


def check_bulk_availability(materials: List[Dict[str, Any]], zip_code: str) -> Dict[str, Any]:
    """
    Check if all materials are available for immediate pickup.
    """
    availability = {
        "all_available": True,
        "items": [],
        "out_of_stock": [],
        "limited_stock": []
    }
    
    for material in materials:
        # Placeholder inventory check
        item_status = {
            "name": material["name"],
            "quantity_requested": material.get("quantity", 1),
            "quantity_available": 10,  # placeholder
            "status": "in_stock"
        }
        
        if item_status["quantity_available"] == 0:
            item_status["status"] = "out_of_stock"
            availability["all_available"] = False
            availability["out_of_stock"].append(item_status)
        elif item_status["quantity_available"] < material.get("quantity", 1):
            item_status["status"] = "limited_stock"
            availability["limited_stock"].append(item_status)
        
        availability["items"].append(item_status)
    
    return availability


def generate_shopping_list_with_links(cabinet_design: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a complete shopping list with store links.
    """
    shopping_list = {
        "materials": [],
        "hardware": [],
        "total_items": 0,
        "estimated_cost": 0,
        "store_links": {
            "home_depot": None,
            "lowes": None
        }
    }
    
    # Extract materials from design
    materials_data = cabinet_design.get("materials", {})
    hardware_data = cabinet_design.get("hardware", {})
    
    # Add materials
    for material, details in materials_data.items():
        shopping_list["materials"].append({
            "name": material,
            "quantity": details.get("quantity", 1),
            "unit": details.get("unit", "sheets"),
            "estimated_price": details.get("price", 50) * details.get("quantity", 1)
        })
    
    # Add hardware
    for hardware_type, details in hardware_data.items():
        shopping_list["hardware"].append({
            "name": hardware_type,
            "quantity": details.get("quantity", 1),
            "unit": "pieces",
            "estimated_price": details.get("price", 5) * details.get("quantity", 1)
        })
    
    # Calculate totals
    shopping_list["total_items"] = len(shopping_list["materials"]) + len(shopping_list["hardware"])
    shopping_list["estimated_cost"] = sum(
        m["estimated_price"] for m in shopping_list["materials"]
    ) + sum(
        h["estimated_price"] for h in shopping_list["hardware"]
    )
    
    # Generate store cart links
    all_items = []
    for material in shopping_list["materials"]:
        product = HOME_DEPOT_PRODUCTS.get(material["name"].lower().replace(" ", "_"))
        if product:
            all_items.append({"sku": product["sku"], "quantity": material["quantity"]})
    
    if all_items:
        shopping_list["store_links"]["home_depot"] = generate_cart_link(all_items, Store.HOME_DEPOT)
    
    return shopping_list


def get_delivery_options(zip_code: str, order_total: float) -> List[Dict[str, Any]]:
    """
    Get delivery options and costs.
    """
    options = [
        {
            "type": "store_pickup",
            "cost": 0,
            "estimated_days": 0,
            "description": "Free pickup at store today"
        },
        {
            "type": "home_delivery",
            "cost": max(0, 79 - (order_total * 0.05)),  # Discount for larger orders
            "estimated_days": 3,
            "description": "Delivery to your driveway"
        },
        {
            "type": "pro_delivery",
            "cost": 29,
            "estimated_days": 1,
            "description": "Priority delivery with placement"
        }
    ]
    
    return options
