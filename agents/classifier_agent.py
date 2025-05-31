import ollama
import re
import json
from typing import Dict, Union

class ClassifierAgent:
    def __init__(self):
        self.model = "llama3"
        self.format_options = ["PDF", "JSON", "Email"]

    def classify(self, input_data: Union[str, bytes]) -> Dict[str, str]:
        """
        Classifies the input data into a format and intent.
        Supports detection via heuristics first, then falls back to LLM if unclear.
        """
        # Step 1: PDF detection (bytes or string)
        if self._is_pdf(input_data):
            return {"format": "PDF", "intent": "Invoice"}

        # Step 2: Decode bytes to string if needed
        if isinstance(input_data, bytes):
            try:
                text_data = input_data.decode('utf-8', errors='replace')
            except Exception:
                return {"format": "unknown", "intent": "Other"}
        else:
            text_data = input_data

        # Step 3: Heuristic detection for JSON and Email
        if self._is_json(text_data):
            return {"format": "JSON", "intent": self._detect_intent(text_data)}
        if self._is_email(text_data):
            return {"format": "Email", "intent": self._detect_intent(text_data)}

        # Step 4: Fallback to LLM classification
        prompt = f"""Classify this input:
{text_data[:2000]}

Respond with STRICT JSON format only:
{{
    "format": "PDF|JSON|Email",
    "intent": "Invoice|RFQ|Complaint|Other"
}}"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": prompt,
                    "format": "json"
                }],
                options={"temperature": 0.1}
            )
            result = json.loads(response["message"]["content"])
            return {
                "format": self._validate_format(result.get("format")),
                "intent": result.get("intent", "Other")
            }
        except Exception as e:
            print(f"LLM error: {e}")
            return {"format": "unknown", "intent": "Other"}

    def _validate_format(self, format: str) -> str:
        """Ensure the format is one of the expected types."""
        if format and format.capitalize() in self.format_options:
            return format.capitalize()
        return "unknown"

    def _is_json(self, text: str) -> bool:
        """Simple heuristic to check if input is likely JSON."""
        text = text.strip()
        return text.startswith(("{", "["))

    def _is_email(self, text: str) -> bool:
        """Detect email-like structure based on 'From:' and 'Subject:' headers."""
        return bool(re.search(r"^From:.+\nSubject:.+", text, re.MULTILINE))

    def _is_pdf(self, data: Union[str, bytes]) -> bool:
        """
        Detect PDF format using binary signature.
        Looks for '%PDF-' at the beginning of the byte stream or string.
        """
        if isinstance(data, bytes):
            return data.startswith(b"%PDF-")
        return data.startswith("%PDF-") or "%PDF-" in data[:1024]

    def _detect_intent(self, text: str) -> str:
        """Basic intent detection using keyword search."""
        text = text.lower()
        if "invoice" in text:
            return "Invoice"
        if "rfq" in text or "quote" in text:
            return "RFQ"
        if "complaint" in text:
            return "Complaint"
        return "Other"
