import asyncio
from typing import Dict, Any

async def check_inventory_and_order(part_name: str, quantity: int = 1) -> Dict[str, Any]:
    """
    Mocks a B2B API call to a local auto parts supplier or hardware depot.
    Simulates network latency to make the stage demo terminal look authentic.
    """
    # Simulate an external API delay of 1.5 seconds
    await asyncio.sleep(1.5)
    
    # Internal routing logic for demo realism
    part_database = {
        "Heavy-duty axle replacement": {"stock": 4, "price": 45000, "location": "Nairobi Industrial Area Depot"},
        "Toyota Land Cruiser 200 Series Brake Pads": {"stock": 12, "price": 18500, "location": "Westlands Branch"},
    }
    
    # Fuzzy matching for the demo
    matched_part = next(
        (key for key in part_database.keys() if part_name.lower() in key.lower()), 
        None
    )
    
    if matched_part:
        details = part_database[matched_part]
        return {
            "status": "confirmed",
            "order_id": "ORD-77X92",
            "pickup_location": details["location"],
            "total_kes": details["price"] * quantity
        }
        
    return {
        "status": "backordered",
        "message": f"Supplier out of stock for {part_name}. ETA 3 days."
    }