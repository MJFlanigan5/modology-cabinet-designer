"""
Phase 5 Localization Feature
- Local supplier search by zip code
- Distance calculation to nearby stores
- Local pricing and availability
- Store inventory integration
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
import math


class StoreType(str, Enum):
    BIG_BOX = "big_box"           # Home Depot, Lowe's, Menards
    HARDWARE_CHAIN = "hardware_chain"  # Ace, True Value
    SPECIALTY_WOODWORKING = "specialty_woodworking"  # Rockler, Woodcraft
    LUMBER_YARD = "lumber_yard"   # Local lumber yards
    ONLINE = "online"             # Online-only suppliers


class SupplierCategory(str, Enum):
    PLYWOOD = "plywood"
    HARDWARE = "hardware"
    TOOLS = "tools"
    FINISHES = "finishes"
    HARDWOOD = "hardwood"
    FASTENERS = "fasteners"
    EDGE_BANDING = "edge_banding"


# Major supplier store locations with coordinates (lat, lng)
SUPPLIER_LOCATIONS = {
    # Big Box Stores
    "home_depot": {
        "name": "Home Depot",
        "type": StoreType.BIG_BOX,
        "base_url": "https://www.homedepot.com",
        "store_locator": "https://www.homedepot.com/l/",
        "api_available": True,
        "categories": [SupplierCategory.PLYWOOD, SupplierCategory.HARDWARE, SupplierCategory.TOOLS, SupplierCategory.FASTENERS],
        "price_tier": "budget",
    },
    "lowes": {
        "name": "Lowe's",
        "type": StoreType.BIG_BOX,
        "base_url": "https://www.lowes.com",
        "store_locator": "https://www.lowes.com/store-locator",
        "api_available": True,
        "categories": [SupplierCategory.PLYWOOD, SupplierCategory.HARDWARE, SupplierCategory.TOOLS, SupplierCategory.FASTENERS],
        "price_tier": "budget",
    },
    "menards": {
        "name": "Menards",
        "type": StoreType.BIG_BOX,
        "base_url": "https://www.menards.com",
        "store_locator": "https://www.menards.com/store-locator",
        "api_available": False,
        "categories": [SupplierCategory.PLYWOOD, SupplierCategory.HARDWARE, SupplierCategory.TOOLS, SupplierCategory.HARDWOOD],
        "price_tier": "budget",
        "regions": ["midwest"],  # Primarily Midwest
    },
    "ace_hardware": {
        "name": "Ace Hardware",
        "type": StoreType.HARDWARE_CHAIN,
        "base_url": "https://www.acehardware.com",
        "store_locator": "https://www.acehardware.com/store-locator",
        "api_available": False,
        "categories": [SupplierCategory.HARDWARE, SupplierCategory.FASTENERS, SupplierCategory.TOOLS],
        "price_tier": "mid",
    },
    "true_value": {
        "name": "True Value",
        "type": StoreType.HARDWARE_CHAIN,
        "base_url": "https://www.truevalue.com",
        "store_locator": "https://www.truevalue.com/store-locator",
        "api_available": False,
        "categories": [SupplierCategory.HARDWARE, SupplierCategory.FASTENERS, SupplierCategory.TOOLS],
        "price_tier": "mid",
    },
    
    # Specialty Woodworking
    "rockler": {
        "name": "Rockler",
        "type": StoreType.SPECIALTY_WOODWORKING,
        "base_url": "https://www.rockler.com",
        "store_locator": "https://www.rockler.com/retail-stores",
        "api_available": False,
        "categories": [SupplierCategory.HARDWOOD, SupplierCategory.HARDWARE, SupplierCategory.TOOLS, SupplierCategory.FINISHES, SupplierCategory.EDGE_BANDING],
        "price_tier": "premium",
        "store_count": 40,  # ~40 retail stores
    },
    "woodcraft": {
        "name": "Woodcraft",
        "type": StoreType.SPECIALTY_WOODWORKING,
        "base_url": "https://www.woodcraft.com",
        "store_locator": "https://www.woodcraft.com/stores",
        "api_available": False,
        "categories": [SupplierCategory.HARDWOOD, SupplierCategory.HARDWARE, SupplierCategory.TOOLS, SupplierCategory.FINISHES],
        "price_tier": "premium",
        "store_count": 80,  # ~80 retail stores
    },
    
    # Lumber Yards (Regional Examples)
    "hardwood_store": {
        "name": "Hardwood Store",
        "type": StoreType.LUMBER_YARD,
        "base_url": "https://www.hardwoodstore.com",
        "api_available": False,
        "categories": [SupplierCategory.HARDWOOD, SupplierCategory.PLYWOOD],
        "price_tier": "mid",
        "regions": ["southeast"],
    },
    "columbia_forest": {
        "name": "Columbia Forest Products",
        "type": StoreType.LUMBER_YARD,
        "base_url": "https://www.cfpwood.com",
        "api_available": False,
        "categories": [SupplierCategory.PLYWOOD, SupplierCategory.HARDWOOD],
        "price_tier": "premium",
    },
    "bell_forest": {
        "name": "Bell Forest Products",
        "type": StoreType.LUMBER_YARD,
        "base_url": "https://www.bellforestproducts.com",
        "api_available": False,
        "categories": [SupplierCategory.HARDWOOD],
        "price_tier": "mid",
    },
    "advantage_lumber": {
        "name": "Advantage Lumber",
        "type": StoreType.LUMBER_YARD,
        "base_url": "https://www.advantagelumber.com",
        "api_available": False,
        "categories": [SupplierCategory.HARDWOOD],
        "price_tier": "mid",
    },
    
    # Specialty Hardware
    "blum": {
        "name": "Blum",
        "type": StoreType.ONLINE,
        "base_url": "https://www.blum.com",
        "api_available": False,
        "categories": [SupplierCategory.HARDWARE],
        "price_tier": "premium",
        "specialty": "hinges and drawer slides",
    },
    "hafele": {
        "name": "Häfele",
        "type": StoreType.ONLINE,
        "base_url": "https://www.hafele.com",
        "api_available": False,
        "categories": [SupplierCategory.HARDWARE],
        "price_tier": "premium",
        "specialty": "cabinet hardware and fittings",
    },
    "mcmaster_carr": {
        "name": "McMaster-Carr",
        "type": StoreType.ONLINE,
        "base_url": "https://www.mcmaster.com",
        "api_available": False,
        "categories": [SupplierCategory.FASTENERS, SupplierCategory.HARDWARE, SupplierCategory.TOOLS],
        "price_tier": "mid",
        "fast_shipping": True,
    },
    "amazon": {
        "name": "Amazon",
        "type": StoreType.ONLINE,
        "base_url": "https://www.amazon.com",
        "api_available": True,
        "categories": [SupplierCategory.HARDWARE, SupplierCategory.TOOLS, SupplierCategory.FINISHES, SupplierCategory.FASTENERS],
        "price_tier": "varies",
    },
}

# Sample store locations for demonstration
# In production, this would be a database or API call
SAMPLE_STORES = [
    # Home Depot locations (sample)
    {"id": "hd_001", "supplier": "home_depot", "name": "Home Depot - Midtown", "lat": 40.7580, "lng": -73.9855, "address": "123 Main St, New York, NY", "phone": "(212) 555-0100"},
    {"id": "hd_002", "supplier": "home_depot", "name": "Home Depot - Brooklyn", "lat": 40.6892, "lng": -73.9857, "address": "456 Atlantic Ave, Brooklyn, NY", "phone": "(718) 555-0200"},
    {"id": "hd_003", "supplier": "home_depot", "name": "Home Depot - Queens", "lat": 40.7282, "lng": -73.7949, "address": "789 Queens Blvd, Queens, NY", "phone": "(347) 555-0300"},
    
    # Lowe's locations (sample)
    {"id": "low_001", "supplier": "lowes", "name": "Lowe's - Manhattan", "lat": 40.7614, "lng": -73.9776, "address": "200 W 23rd St, New York, NY", "phone": "(212) 555-1100"},
    {"id": "low_002", "supplier": "lowes", "name": "Lowe's - Bronx", "lat": 40.8448, "lng": -73.8648, "address": "300 Fordham Rd, Bronx, NY", "phone": "(718) 555-1200"},
    
    # Rockler locations (sample)
    {"id": "rck_001", "supplier": "rockler", "name": "Rockler - New York", "lat": 40.7505, "lng": -73.9934, "address": "55 W 39th St, New York, NY", "phone": "(212) 555-2100"},
    
    # Woodcraft locations (sample)
    {"id": "wcf_001", "supplier": "woodcraft", "name": "Woodcraft - New Jersey", "lat": 40.7891, "lng": -74.0123, "address": "50 Bergen Turnpike, NJ", "phone": "(201) 555-3100"},
    
    # Local lumber yards (sample)
    {"id": "lbr_001", "supplier": "hardwood_store", "name": "NYC Hardwoods", "lat": 40.7128, "lng": -74.0060, "address": "88 Broadway, Brooklyn, NY", "phone": "(718) 555-4100"},
]


class LocalSupplier(BaseModel):
    supplier_id: str
    supplier_key: str
    name: str
    type: StoreType
    distance_miles: float
    address: str
    phone: Optional[str] = None
    lat: float
    lng: float
    categories: List[SupplierCategory]
    price_tier: str
    store_url: Optional[str] = None
    search_url: str
    available_categories: List[str]
    in_stock_probability: Optional[float] = None


class LocalSearchResult(BaseModel):
    zip_code: str
    coordinates: tuple
    suppliers: List[LocalSupplier]
    total_count: int
    by_type: Dict[str, int]
    by_category: Dict[str, List[LocalSupplier]]
    recommendations: List[str]


def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate distance between two coordinates in miles.
    
    Uses the Haversine formula for accurate distance calculation.
    """
    
    R = 3959  # Earth's radius in miles
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    
    a = math.sin(delta_lat / 2) ** 2 + \
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def get_coordinates_from_zip(zip_code: str) -> tuple:
    """
    Get latitude and longitude from US zip code.
    
    In production, this would use a geocoding API like Google Maps or OpenStreetMap.
    For now, returns approximate coordinates for common zip prefixes.
    """
    
    # Sample zip code to coordinate mapping (first 3 digits)
    # In production, use actual geocoding API
    zip_prefix_map = {
        "100": (40.7580, -73.9855),  # NYC Manhattan
        "101": (40.7614, -73.9776),  # NYC Midtown
        "102": (40.7061, -74.0087),  # NYC Financial District
        "103": (40.5834, -74.1496),  # Staten Island
        "104": (40.8448, -73.8648),  # Bronx
        "105": (41.2621, -73.7990),  # Westchester
        "106": (41.0891, -73.8168),  # Westchester
        "107": (40.9292, -73.8726),  # Yonkers
        "108": (40.7965, -73.4821),  # Long Island
        "109": (41.1510, -74.0329),  # Rockland
        "110": (40.7554, -73.6798),  # Long Island
        "111": (40.7401, -73.7860),  # Queens
        "112": (40.6501, -73.9496),  # Brooklyn
        "113": (40.7282, -73.7949),  # Queens
        "114": (40.7214, -73.8445),  # Queens
        "115": (40.6634, -73.7353),  # Long Island
        "116": (40.5886, -73.7932),  # Rockaway
        "117": (40.7884, -73.1042),  # Long Island
        "118": (40.7572, -73.4201),  # Long Island
        "119": (40.9223, -72.6371),  # Suffolk
        
        # California
        "900": (34.0522, -118.2437),  # Los Angeles
        "902": (34.0195, -118.4912),  # Santa Monica
        "904": (34.0195, -118.4912),  # Santa Monica
        "906": (33.9592, -118.1387),  # Downey
        "908": (33.7701, -118.1937),  # Long Beach
        "910": (34.1478, -118.1445),  # Pasadena
        "912": (34.1478, -118.1445),  # Glendale
        "914": (34.1808, -118.3080),  # Van Nuys
        "916": (34.1808, -118.3080),  # North Hollywood
        "917": (34.0195, -118.4912),  # Various LA
        "918": (34.0195, -118.4912),  # Various LA
        "919": (32.7157, -117.1611),  # San Diego
        "920": (32.7157, -117.1611),  # San Diego
        "921": (32.7157, -117.1611),  # San Diego
        "922": (33.7206, -116.2156),  # Palm Springs
        "923": (34.1083, -117.2938),  # San Bernardino
        "924": (34.1083, -117.2938),  # San Bernardino
        "925": (33.9533, -117.3962),  # Riverside
        "926": (33.6595, -117.8191),  # Orange County
        "927": (33.8360, -117.8789),  # Orange County
        "928": (33.8360, -117.8789),  # Orange County
        "930": (34.2778, -119.2932),  # Ventura
        "931": (34.4208, -119.6982),  # Santa Barbara
        "932": (36.2404, -119.8110),  # Tulare
        "933": (35.3733, -119.0187),  # Bakersfield
        "934": (35.2828, -120.6596),  # San Luis Obispo
        "935": (35.3733, -119.0187),  # Mojave
        "936": (36.7468, -119.7726),  # Fresno
        "937": (36.7468, -119.7726),  # Fresno
        "940": (37.4419, -122.1430),  # Palo Alto
        "941": (37.7749, -122.4194),  # San Francisco
        "942": (37.7749, -122.4194),  # San Francisco
        "943": (37.4419, -122.1430),  # Palo Alto
        "944": (37.5630, -122.3255),  # San Mateo
        "945": (37.6624, -121.8747),  # East Bay
        "946": (37.8044, -122.2712),  # Oakland
        "947": (37.8654, -122.2587),  # Berkeley
        "948": (37.9358, -122.3477),  # Richmond
        "949": (38.0494, -122.7677),  # Marin
        "950": (37.3541, -121.9552),  # San Jose
        "951": (37.3382, -121.8863),  # San Jose
        "952": (37.9577, -121.2908),  # Stockton
        "953": (37.6391, -120.9969),  # Modesto
        "954": (38.4404, -122.7141),  # Sonoma
        "955": (40.8021, -124.1507),  # Humboldt
        "956": (38.5816, -121.4944),  # Sacramento
        "957": (38.5816, -121.4944),  # Sacramento
        "958": (38.5816, -121.4944),  # Sacramento
        "959": (39.7384, -121.8350),  # Chico
        
        # Texas
        "750": (33.1507, -96.8235),   # Dallas area
        "751": (32.7767, -96.7970),   # Dallas
        "752": (32.7767, -96.7970),   # Dallas
        "754": (33.1972, -96.6397),   # McKinney
        "756": (32.5007, -94.7405),   # Longview
        "757": (32.5007, -94.7405),   # Tyler
        "758": (31.5496, -95.0677),   # Palestine
        "759": (31.0982, -95.1283),   # Livingston
        "760": (32.7357, -97.1081),   # Arlington
        "761": (32.7555, -97.3327),   # Fort Worth
        "762": (33.2148, -97.1331),   # Denton
        "763": (33.9137, -98.4934),   # Wichita Falls
        "764": (31.5496, -95.0677),   # Central TX
        "765": (31.1070, -97.3547),   # Killeen
        "766": (31.5496, -95.0677),   # Waco
        "767": (31.5496, -95.0677),   # Waco
        "768": (31.5496, -95.0677),   # Central TX
        "769": (31.4248, -100.4623),  # San Angelo
        "770": (29.7604, -95.3698),   # Houston
        "771": (29.7604, -95.3698),   # Houston
        "772": (29.7604, -95.3698),   # Houston
        "773": (30.0956, -95.3985),   # Conroe
        "774": (29.6197, -95.6349),   # Sugar Land
        "775": (29.5608, -95.0677),   # Pasadena
        "776": (30.0819, -94.1316),   # Beaumont
        "777": (30.1077, -94.1373),   # Beaumont
        "778": (30.5858, -96.3047),   # College Station
        "779": (28.8544, -96.9317),   # Victoria
        "780": (29.4241, -98.4936),   # San Antonio
        "781": (29.4241, -98.4936),   # San Antonio
        "782": (29.4241, -98.4936),   # San Antonio
        "783": (27.8006, -97.3964),   # Corpus Christi
        "784": (27.8006, -97.3964),   # Corpus Christi
        "785": (26.1901, -98.2343),   # McAllen
        "786": (30.2362, -97.7458),   # Austin
        "787": (30.2672, -97.7431),   # Austin
        "788": (29.5645, -100.4015),  # Del Rio
        "789": (29.9296, -96.9033),   # La Grange
        "790": (34.9476, -102.2523),  # Lubbock
        "791": (33.5779, -101.8552),  # Lubbock
        "792": (34.1804, -100.2857),  # Vernon
        "793": (33.5779, -101.8552),  # Plainview
        "794": (33.5779, -101.8552),  # Lubbock
        "795": (32.4487, -99.7331),   # Abilene
        "796": (32.4487, -99.7331),   # Abilene
        "797": (31.9973, -102.0779),  # Midland/Odessa
        "798": (31.8457, -102.3666),  # Fort Davis
        "799": (31.7619, -106.4850),  # El Paso
        
        # Florida
        "320": (30.3322, -81.6557),   # Jacksonville
        "321": (29.0244, -81.3273),   # Daytona Beach
        "322": (30.3322, -81.6557),   # Jacksonville
        "323": (30.4383, -84.2807),   # Tallahassee
        "324": (30.1595, -85.6598),   # Panama City
        "325": (30.4213, -87.2169),   # Pensacola
        "326": (29.6516, -82.3248),   # Gainesville
        "327": (28.5383, -81.3792),   # Orlando
        "328": (28.5383, -81.3792),   # Orlando
        "329": (28.0836, -80.6081),   # Melbourne
        "330": (26.1223, -80.1434),   # Fort Lauderdale
        "331": (25.7617, -80.1918),   # Miami
        "332": (25.7617, -80.1918),   # Miami
        "333": (26.1223, -80.1434),   # Fort Lauderdale
        "334": (26.7153, -80.0534),   # West Palm Beach
        "335": (27.9506, -82.4572),   # Tampa
        "336": (27.9506, -82.4572),   # Tampa
        "337": (27.7676, -82.6403),   # St Petersburg
        "338": (28.0345, -81.9498),   # Lakeland
        "339": (26.6406, -81.8723),   # Fort Myers
        "340": (25.0300, -77.1033),   # Bahamas (for reference)
        "341": (26.1420, -81.7948),   # Naples
        "342": (27.3364, -82.5306),   # Sarasota
        "344": (29.1872, -82.1365),   # Ocala
        "346": (28.3382, -82.2561),   # Spring Hill
        "347": (28.3851, -81.4249),   # Kissimmee
        "349": (27.1980, -80.2466),   # Port St Lucie
        "350": (33.5207, -86.8025),   # Birmingham
        "351": (33.5207, -86.8025),   # Birmingham
        "352": (34.1807, -86.8025),   # North AL
        "354": (33.2098, -87.5692),   # Tuscaloosa
        "355": (34.0007, -87.5322),   # Jasper
        "356": (34.6059, -87.0287),   # Florence
        "357": (34.7543, -86.6986),   # Huntsville
        "358": (34.7304, -86.5861),   # Huntsville
        "359": (33.8254, -85.7636),   # Anniston
        "360": (32.3668, -86.3000),   # Montgomery
        "361": (32.3668, -86.3000),   # Montgomery
        "363": (31.2233, -85.3883),   # Dothan
        "364": (31.3152, -86.4783),   # Andalusia
        "365": (30.6954, -88.0399),   # Mobile
        "366": (30.6954, -88.0399),   # Mobile
        "368": (32.6099, -85.4788),   # Auburn
    }
    
    # Get prefix (first 3 digits)
    prefix = zip_code[:3]
    
    # Return coordinates or default to NYC
    if prefix in zip_prefix_map:
        return zip_prefix_map[prefix]
    else:
        # Default to center of US for unknown zip codes
        return (39.8283, -98.5795)


def find_local_suppliers(
    zip_code: str,
    radius_miles: float = 25.0,
    categories: List[SupplierCategory] = None,
    store_types: List[StoreType] = None,
    max_results: int = 20,
) -> LocalSearchResult:
    """
    Find local suppliers near a zip code.
    
    Args:
        zip_code: US zip code
        radius_miles: Search radius in miles
        categories: Filter by supplier categories
        store_types: Filter by store types
        max_results: Maximum number of results
    
    Returns:
        LocalSearchResult with nearby suppliers
    """
    
    # Get coordinates from zip code
    user_lat, user_lng = get_coordinates_from_zip(zip_code)
    
    # Find stores within radius
    nearby_stores = []
    
    for store in SAMPLE_STORES:
        distance = haversine_distance(
            user_lat, user_lng,
            store["lat"], store["lng"]
        )
        
        if distance <= radius_miles:
            supplier_info = SUPPLIER_LOCATIONS.get(store["supplier"], {})
            
            # Filter by store type
            if store_types and supplier_info.get("type") not in store_types:
                continue
            
            # Filter by category
            supplier_categories = supplier_info.get("categories", [])
            if categories:
                if not any(cat in supplier_categories for cat in categories):
                    continue
            
            nearby_stores.append(LocalSupplier(
                supplier_id=store["id"],
                supplier_key=store["supplier"],
                name=store["name"],
                type=supplier_info.get("type", StoreType.ONLINE),
                distance_miles=round(distance, 2),
                address=store["address"],
                phone=store.get("phone"),
                lat=store["lat"],
                lng=store["lng"],
                categories=supplier_categories,
                price_tier=supplier_info.get("price_tier", "mid"),
                store_url=f"{supplier_info.get('base_url', '')}",
                search_url=f"{supplier_info.get('base_url', '')}/search?q=cabinet+hardware",
                available_categories=[cat.value for cat in supplier_categories],
                in_stock_probability=_estimate_stock_probability(distance, supplier_info.get("type")),
            ))
    
    # Sort by distance
    nearby_stores.sort(key=lambda x: x.distance_miles)
    
    # Limit results
    nearby_stores = nearby_stores[:max_results]
    
    # Group by type
    by_type = {}
    for store in nearby_stores:
        type_key = store.type.value
        by_type[type_key] = by_type.get(type_key, 0) + 1
    
    # Group by category
    by_category = {}
    for store in nearby_stores:
        for cat in store.categories:
            cat_key = cat.value
            if cat_key not in by_category:
                by_category[cat_key] = []
            by_category[cat_key].append(store)
    
    # Generate recommendations
    recommendations = _generate_local_recommendations(nearby_stores, categories)
    
    return LocalSearchResult(
        zip_code=zip_code,
        coordinates=(user_lat, user_lng),
        suppliers=nearby_stores,
        total_count=len(nearby_stores),
        by_type=by_type,
        by_category=by_category,
        recommendations=recommendations,
    )


def _estimate_stock_probability(distance: float, store_type: StoreType) -> float:
    """Estimate probability of item being in stock."""
    
    # Big box stores have high stock probability
    if store_type == StoreType.BIG_BOX:
        return 0.85
    elif store_type == StoreType.SPECIALTY_WOODWORKING:
        return 0.75
    elif store_type == StoreType.LUMBER_YARD:
        return 0.70
    else:
        return 0.80


def _generate_local_recommendations(
    stores: List[LocalSupplier],
    requested_categories: List[SupplierCategory],
) -> List[str]:
    """Generate personalized recommendations based on nearby stores."""
    
    recommendations = []
    
    if not stores:
        recommendations.append("No stores found in your area. Consider online suppliers like Amazon or McMaster-Carr.")
        return recommendations
    
    # Check for specialty stores
    specialty_stores = [s for s in stores if s.type == StoreType.SPECIALTY_WOODWORKING]
    if specialty_stores:
        recommendations.append(
            f"🎯 Great! You have {len(specialty_stores)} specialty woodworking store(s) nearby: " +
            ", ".join([s.name for s in specialty_stores[:2]])
        )
    
    # Check for big box stores
    big_box = [s for s in stores if s.type == StoreType.BIG_BOX]
    if big_box and requested_categories:
        if SupplierCategory.PLYWOOD in requested_categories:
            recommendations.append(
                f"📦 For plywood, check {big_box[0].name} ({big_box[0].distance_miles} mi) - usually good stock and prices"
            )
        if SupplierCategory.HARDWARE in requested_categories:
            recommendations.append(
                f"🔧 For basic hardware, {big_box[0].name} has good selection. For specialty hardware, check online suppliers."
            )
    
    # Check for lumber yards
    lumber_yards = [s for s in stores if s.type == StoreType.LUMBER_YARD]
    if lumber_yards and SupplierCategory.HARDWOOD in (requested_categories or []):
        recommendations.append(
            f"🪵 For hardwoods, visit {lumber_yards[0].name} - better selection than big box stores"
        )
    
    # Price comparison tip
    if len(stores) >= 2:
        budget_stores = [s for s in stores if s.price_tier == "budget"]
        premium_stores = [s for s in stores if s.price_tier == "premium"]
        if budget_stores and premium_stores:
            recommendations.append(
                f"💡 Tip: Compare prices! {budget_stores[0].name} for basics, {premium_stores[0].name} for quality/specialty items"
            )
    
    # Distance-based recommendations
    closest = stores[0] if stores else None
    if closest and closest.distance_miles > 15:
        recommendations.append(
            f"📍 Nearest store is {closest.distance_miles} miles away. Consider calling ahead to check inventory!"
        )
    
    return recommendations


def get_supplier_search_links(
    zip_code: str,
    search_terms: List[str],
    suppliers: List[str] = None,
) -> Dict[str, List[Dict[str, str]]]:
    """
    Generate direct search links for each supplier.
    
    Args:
        zip_code: User's zip code for context
        search_terms: Items to search for
        suppliers: Specific suppliers to include (None = all)
    
    Returns:
        Dictionary of supplier -> search links
    """
    
    results = {}
    
    for supplier_key, supplier_info in SUPPLIER_LOCATIONS.items():
        if suppliers and supplier_key not in suppliers:
            continue
        
        base_url = supplier_info.get("base_url", "")
        links = []
        
        for term in search_terms:
            # URL encode the search term
            encoded_term = term.replace(" ", "+")
            
            # Generate search URL based on supplier
            if supplier_key == "home_depot":
                search_url = f"{base_url}/s/{encoded_term}?searchtype=search"
            elif supplier_key == "lowes":
                search_url = f"{base_url}/search?searchTerm={encoded_term}"
            elif supplier_key == "amazon":
                search_url = f"{base_url}/s?k={encoded_term}"
            elif supplier_key == "rockler":
                search_url = f"{base_url}/search?q={encoded_term}"
            elif supplier_key == "woodcraft":
                search_url = f"{base_url}/search?q={encoded_term}"
            else:
                search_url = f"{base_url}/search?q={encoded_term}"
            
            links.append({
                "search_term": term,
                "url": search_url,
            })
        
        results[supplier_key] = {
            "name": supplier_info.get("name"),
            "type": supplier_info.get("type").value if supplier_info.get("type") else None,
            "search_links": links,
        }
    
    return results


def compare_local_prices(
    zip_code: str,
    item_name: str,
    category: SupplierCategory = None,
) -> Dict[str, Any]:
    """
    Compare prices for an item across local suppliers.
    
    Args:
        zip_code: User's zip code
        item_name: Item to compare prices for
        category: Item category for filtering
    
    Returns:
        Price comparison results
    """
    
    # Find nearby stores
    local_result = find_local_suppliers(
        zip_code=zip_code,
        radius_miles=25.0,
        categories=[category] if category else None,
    )
    
    # Generate search links for all suppliers
    all_links = get_supplier_search_links(zip_code, [item_name])
    
    # Match local stores with links
    price_comparison = {
        "item": item_name,
        "category": category.value if category else None,
        "zip_code": zip_code,
        "local_stores": [],
        "online_options": [],
        "recommendations": [],
    }
    
    for store in local_result.suppliers:
        supplier_data = all_links.get(store.supplier_key, {})
        search_link = supplier_data.get("search_links", [{}])[0].get("url", "")
        
        price_comparison["local_stores"].append({
            "store_name": store.name,
            "distance": store.distance_miles,
            "address": store.address,
            "phone": store.phone,
            "price_tier": store.price_tier,
            "in_stock_probability": store.in_stock_probability,
            "search_link": search_link,
        })
    
    # Add online options
    online_suppliers = ["amazon", "mcmaster_carr"]
    for supplier_key in online_suppliers:
        if supplier_key in all_links:
            supplier_data = all_links[supplier_key]
            price_comparison["online_options"].append({
                "name": supplier_data["name"],
                "search_link": supplier_data["search_links"][0]["url"] if supplier_data["search_links"] else None,
                "fast_shipping": supplier_key == "mcmaster_carr",
            })
    
    # Generate recommendations
    if price_comparison["local_stores"]:
        closest = price_comparison["local_stores"][0]
        price_comparison["recommendations"].append(
            f"Closest option: {closest['store_name']} ({closest['distance']} mi)"
        )
    
    price_comparison["recommendations"].append(
        "Check prices online before driving - big box stores often price-match!"
    )
    
    return price_comparison


def get_local_inventory_status(
    zip_code: str,
    item_name: str,
    supplier_key: str,
) -> Dict[str, Any]:
    """
    Check local inventory status for an item.
    
    Note: In production, this would connect to store APIs.
    For now, returns estimated availability.
    
    Args:
        zip_code: User's zip code
        item_name: Item to check
        supplier_key: Supplier identifier
    
    Returns:
        Inventory status information
    """
    
    supplier_info = SUPPLIER_LOCATIONS.get(supplier_key, {})
    
    return {
        "item": item_name,
        "supplier": supplier_info.get("name", supplier_key),
        "zip_code": zip_code,
        "status": "unknown",
        "message": "Inventory check requires store API integration",
        "suggestion": f"Call ahead or check {supplier_info.get('base_url', '')} for availability",
        "api_available": supplier_info.get("api_available", False),
    }
