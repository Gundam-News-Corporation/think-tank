import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"
REPORTS_DIR = DOCS_DIR / "reports"
API_DIR = REPORTS_DIR / "API"

class ThinkTankRouter:
    """
    Automated classification router that assigns exact category IDs
    verified from the live Joomla 6 database backend.
    """
    def __init__(self):
        # Master routing array linking search keywords to live category IDs
        self.category_mapping = {
            "manual": 9,
            "sop": 9,
            "procurement": 10,
            "contract": 10,
            "hurricane": 11,
            "logistics": 11,
            "maxwell": 13,
            "beam cannon": 13,
            "plasma": 13,
            "antigravity": 14,
            "induction": 14,
            "gravity": 14,
            "hexadecimal": 15,
            "circuit": 15,
            "snap": 15,
            "qubit": 15,
            "hardware": 16,
            "bridge": 16,
            "infestation": 18,
            "containment": 18,
            "rodent": 18,
            "plant": 19,
            "biosecurity": 19,
            "cold-chain": 20,
            "telemetry": 20
        }

    def determine_category(self, text_payload: str) -> int:
        """
        Parses text parameters and determines the matching target category.
        Defaults to General News (ID 2) if no key signature is detected.
        """
        lower_text = text_payload.lower()
        for keyword, cat_id in self.category_mapping.items():
            if keyword in lower_text:
                return cat_id
        return 2  # Fallback: General News Category from user layout

    def build_api_payload(self, title: str, markdown_body: str, clean_html: str):
        """
        Assembles a valid article payload and writes it directly to docs/reports/API/
        """
        # Determine taxonomy route automatically
        target_catid = self.determine_category(markdown_body + " " + title)
        
        safe_filename = title.lower().replace(" ", "_").replace(":", "")
        
        # Save structural markdown copy
        md_file = REPORTS_DIR / f"{safe_filename}.md"
        md_file.write_text(markdown_body, encoding="utf-8")
        
        # Assemble Joomla 6 Core Web Services compatible data format
        payload = {
            "title": title,
            "alias": safe_filename.replace("_", "-"),
            "catid": target_catid,
            "articletext": clean_html,
            "state": 1,         # 1 = Published instantly
            "access": 1,        # 1 = Public viewing permissions
            "created_by": 151,  # Set directly to Univac Controller ID from your screenshot
            "language": "*"     # All languages accessible
        }
        
        json_file = API_DIR / f"payload_{safe_filename}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)
            
        print(f"🎯 Structured payload for '{title}' mapped to Category ID: {target_catid}")
