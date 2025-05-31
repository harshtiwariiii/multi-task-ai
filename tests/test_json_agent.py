import pytest
import json
from agents.json_agent import JSONAgent

# Sample test schemas and data
VALID_INVOICE = {
    "invoice_id": "INV-2023-001",
    "due_date": "2023-12-31",
    "amount": 1000.00,
    "customer": "Flowbit Inc."
}

MISSING_FIELD_INVOICE = {
    "due_date": "2023-12-31",  # Missing required 'invoice_id'
    "amount": 1000.00
}

INVALID_TYPE_INVOICE = {
    "invoice_id": 12345,  # Should be string
    "due_date": "2023-12-31"
}

@pytest.fixture
def invoice_schema():
    """Load the invoice schema for testing"""
    return {
        "type": "object",
        "properties": {
            "invoice_id": {"type": "string"},
            "due_date": {"type": "string", "format": "date"},
            "amount": {"type": "number"},
            "customer": {"type": "string"}
        },
        "required": ["invoice_id", "due_date"]
    }

@pytest.fixture
def json_agent(invoice_schema):
    """Create a JSONAgent instance with the test schema"""
    return JSONAgent(schema=invoice_schema)

def test_valid_json(json_agent):
    """Test validation of perfectly valid JSON"""
    result = json_agent.validate(VALID_INVOICE)
    assert result["status"] == "valid"
    assert "data" in result
    assert result["data"]["invoice_id"] == "INV-2023-001"

def test_missing_required_field(json_agent):
    """Test detection of missing required field"""
    result = json_agent.validate(MISSING_FIELD_INVOICE)
    assert result["status"] == "error"
    assert "missing 'invoice_id'" in result["message"].lower()

def test_invalid_field_type(json_agent):
    """Test detection of incorrect field types"""
    result = json_agent.validate(INVALID_TYPE_INVOICE)
    assert result["status"] == "error"
    assert "12345 is not of type 'string'" in result["message"]

def test_additional_properties(json_agent):
    """Test that extra fields don't cause validation errors"""
    test_data = VALID_INVOICE.copy()
    test_data["extra_field"] = "should be allowed"
    result = json_agent.validate(test_data)
    assert result["status"] == "valid"

def test_empty_json(json_agent):
    """Test handling of empty JSON object"""
    result = json_agent.validate({})
    assert result["status"] == "error"
    assert "missing properties" in result["message"].lower()

def test_null_values(json_agent):
    """Test handling of null values"""
    test_data = VALID_INVOICE.copy()
    test_data["customer"] = None
    result = json_agent.validate(test_data)
    assert result["status"] == "valid"  # Assuming null is allowed unless forbidden in schema