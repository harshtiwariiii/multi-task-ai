import re
import json
from typing import Dict

class EmailAgent:
    def parse(self, email_text: str) -> Dict[str, str]:
        try:
            # Extract headers
            sender = re.search(r"From:\s*(.+)", email_text).group(1).strip()
            subject = re.search(r"Subject:\s*(.+)", email_text).group(1).strip()
            
            # Simple body extraction
            body = email_text.split("\n\n", 1)[-1][:500]
            
            return {
                "sender": sender,
                "subject": subject,
                "body_preview": body,
                "status": "processed"
            }
        except Exception as e:
            return {
                "error": f"Email parsing failed: {str(e)}",
                "status": "failed"
            }