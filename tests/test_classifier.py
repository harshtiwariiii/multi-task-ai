from agents.classifier_agent import ClassifierAgent

def test_classifier_initialization():
    """Test if ClassifierAgent initializes correctly"""
    agent = ClassifierAgent()
    assert agent is not None

def test_classify_email():
    """Test email classification"""
    agent = ClassifierAgent()
    result = agent.classify("From: test@example.com\nSubject: Invoice")
    assert result["format"] == "Email"
    assert "intent" in result