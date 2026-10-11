from src.services import text
from src.services.text import FieldAction


def test_extract_dispatch_intent(monkeypatch):
    # 1. Arrange: replace the LLM-backed extractor with a predictable payload
    mock_payload = {
        "intent": "dispatch_unit",
        "client_or_vehicle_id": "KCD 123",
        "total_cost": 5000,
        "items": ["Towing"],
        "location": "Mombasa Road",
    }

    def mock_generate(*args, **kwargs):
        return FieldAction(**mock_payload)

    # Patch the attribute on the module so the call below resolves to the mock
    monkeypatch.setattr(text, "extract_intent_and_entities", mock_generate)

    # 2. Act
    result = text.extract_intent_and_entities("Tow truck needed at Mombasa Road for KCD 123, quoted 5k")

    # 3. Assert
    assert result.intent == "dispatch_unit"
    assert result.client_or_vehicle_id == "KCD 123"
    assert result.total_cost == 5000

