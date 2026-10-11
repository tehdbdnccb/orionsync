import json
from pydantic import BaseModel, Field
from typing import List, Optional
# from src.adapters.groq_client import generate_structured_json
# from src.utils.logger import log

class FieldAction(BaseModel):
    intent: str = Field(..., description="The primary action: 'generate_quote', 'dispatch_unit', or 'order_parts'")
    client_or_vehicle_id: str = Field(..., description="Name of the client, company, or vehicle license plate")
    total_cost: Optional[int] = Field(None, description="Total cost in local currency if mentioned")
    items: List[str] = Field(default_factory=list, description="List of specific parts or services requested")
    location: Optional[str] = Field(None, description="Physical location or highway marker")

def extract_intent_and_entities(raw_text: str) -> FieldAction:
    """
    Passes the transcribed text to the LLM to extract a structured JSON payload.
    """
    # log.info(f"Extracting entities from text: {raw_text[:50]}...")
    
    # In production, this calls OpenAI with structured outputs (JSON mode).
    # mock_json_string = generate_structured_json(raw_text, schema=FieldAction.schema())
    
    # Mocking the LLM extraction for the hackathon demo context
    mock_llm_response = {
        "intent": "dispatch_unit",
        "client_or_vehicle_id": "KCD 456X",
        "total_cost": 45000,
        "items": ["Heavy-duty axle replacement", "Towing service"],
        "location": "A104 Highway, near Naivasha weighbridge"
    }
    
    # Validates and parses the dictionary into our Pydantic model
    return FieldAction(**mock_llm_response)