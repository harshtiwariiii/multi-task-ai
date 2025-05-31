# pdf_agent.py
import pdfplumber
import re
from typing import Dict

class PDFAgent:
    def extract(self, filepath: str) -> Dict[str, any]:
        try:
            with pdfplumber.open(filepath) as pdf:
                # Extract text from first page
                first_page = pdf.pages[0]
                text = first_page.extract_text()
                
                # Parse invoice data
                invoice_data = {
                    "invoice_number": self._extract_field(text, "Invoice Number:"),
                    "date": self._extract_field(text, "Date:"),
                    "due_date": self._extract_field(text, "Due Date:"),
                    "bill_to": self._extract_field(text, "Bill To:"),
                    "total_amount": self._extract_field(text, "Total Due:"),
                    "line_items": self._extract_line_items(text)
                }
                
                return {
                    "status": "processed",
                    "type": "invoice",
                    "data": invoice_data
                }
                
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }

    def _extract_field(self, text: str, field_name: str) -> str:
        """Extracts value after a field label"""
        match = re.search(rf"{field_name}\s*(.+)", text)
        return match.group(1).strip() if match else ""

    def _extract_line_items(self, text: str) -> list:
        """Extracts line items between the table header and total"""
        items = []
        table_start = re.search(r"Description\s+Qty\s+Unit Price\s+Total", text)
        table_end = re.search(r"Total Due:", text)
        
        if table_start and table_end:
            table_text = text[table_start.end():table_end.start()]
            for line in table_text.split('\n'):
                if line.strip() and not line.startswith('---'):
                    parts = re.split(r'\s{2,}', line.strip())
                    if len(parts) >= 4:
                        items.append({
                            "description": parts[0],
                            "quantity": parts[1],
                            "unit_price": parts[2],
                            "total": parts[3]
                        })
        return items