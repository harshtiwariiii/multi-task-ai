from agents.classifier_agent import ClassifierAgent
from agents.json_agent import JSONAgent
from agents.email_agent import EmailAgent
from agents.pdf_agent import PDFAgent  # New PDF agent
from memory.shared_memory import SharedMemory
import json
import sys
from pathlib import Path
import hashlib

def process_input(input_data: str = "", input_source: str = None) -> dict:
    """Process input with format auto-detection and proper error handling"""
    # Initialize components
    classifier = ClassifierAgent()
    memory = SharedMemory()
    
    # Handle file input
    # Change the file reading block to:
    if input_source:
     try:
        with open(input_source, 'r', encoding='utf-8') as f:
            input_data = f.read(20000)
     except (UnicodeDecodeError, PermissionError):
        try:
            with open(input_source, 'rb') as f:
                input_data = f.read(20000)
        except Exception as e:
            return {
                "error": f"Failed to read file: {str(e)}",
                "status": "failed"
            }

    if isinstance(input_data, bytes):
       request_id = f"req_{hashlib.md5(input_data).hexdigest()[:8]}"
    else:
       request_id = f"req_{hashlib.md5(input_data.encode()).hexdigest()[:8]}"

    try:
        # Classify input (handles both bytes and str)
        classification = classifier.classify(input_data)
        
        # Prepare input sample snippet (decode bytes safely)
        input_sample = input_data[:200]
        if isinstance(input_sample, bytes):
            try:
                input_sample = input_sample.decode(errors='replace')
            except Exception:
                input_sample = str(input_sample)

        memory.log(
            request_id=request_id,
            stage="classification",
            data={
                "format": classification.get("format"),
                "intent": classification.get("intent"),
                "input_sample": input_sample
            }
        )

        # Process based on detected format
        result = {"status": "unprocessed"}
        format = classification.get("format", "").upper()

        if format == "JSON":
            agent = JSONAgent("schemas/invoice_schema.json")
            json_data = input_data.decode() if isinstance(input_data, bytes) else input_data
            result = agent.validate(json.loads(json_data))
        elif format == "EMAIL":
            agent = EmailAgent()
            text = input_data.decode() if isinstance(input_data, bytes) else input_data
            result = agent.parse(text)
        elif format == "PDF":
            agent = PDFAgent()
            # PDF processing expects file path
            result = agent.extract(input_source)
        else:
            result["error"] = f"Unsupported format: {format}"

        memory.log(
            request_id=request_id,
            stage="processing",
            data=result
        )

        return {
            "request_id": request_id,
            "classification": classification,
            "result": result
        }

    except json.JSONDecodeError as e:
        return {
            "request_id": request_id,
            "error": f"Invalid JSON: {str(e)}",
            "status": "failed"
        }
    except Exception as e:
        return {
            "request_id": request_id,
            "error": str(e),
            "status": "failed"
        }


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--input":
        input_path = sys.argv[2]
        print(f"Processing {input_path}:")
        result = process_input(input_source=input_path)
        print(json.dumps(result, indent=2))
    else:
        # Test cases
        print("Email Test:")
        print(json.dumps(
            process_input("From: client@example.com\nSubject: Invoice #123\n\nPlease pay by 2023-12-31"),
            indent=2
        ))
        
        print("\nJSON Test:")
        print(json.dumps(
            process_input('{"invoice_id": "INV-123", "amount": 1000.00}'),
            indent=2
        ))
        
        print("\nPDF Test:")
        print(json.dumps(
            process_input(input_source="samples/invoice.pdf"),  # Requires PDFAgent
            indent=2
        ))