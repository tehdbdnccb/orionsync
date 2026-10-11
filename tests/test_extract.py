import pytest
from src.services.text import extract_intent_and_entities, FieldAction

def test_extract_dispatch_intent(monkeypatch: pytest.MonkeyPatch):
    # 1. Arrange: Mock the LLM adapter to return a predictable dictionary
    mock_payload = {
        "intent": "dispatch_unit",
        "client_or_vehicle_id": "KCD 123",
        "total_cost": 5000,
        "items": ["Towing"],
        "location": "Mombasa Road"
    }
    
    def mock_generate(*args, **kwargs):
        return FieldAction(**mock_payload)
        
    monkeypatch.setattr("src.services.text.extract_intent_and_entities", mock_generate)

    # 2. Act
    result = extract_intent_and_entities("Tow truck needed at Mombasa Road for KCD 123, quoted 5k")

    # 3. Assert
    assert result.intent == "dispatch_unit"
    assert result.client_or_vehicle_id == "KCD 123"
    assert result.total_cost == 5000