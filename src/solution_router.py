import json
from pathlib import Path

# Path definitions
ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"
REPORTS_DIR = DOCS_DIR / "reports"
API_DIR = REPORTS_DIR / "API"

class ThinkTankRouter:
    """
    Automated resolution engine matching vetted intelligence alerts 
    against proprietary defense systems at https://gundam.solutions
    """
    def __init__(self):
        self.registry_payload = []

    def classify_and_route(self, threat_source: str, alert_text: str):
        """
        Ingests raw text feeds and maps them to specialized technical nodes.
        """
        solution_metadata = {}
        
        # Scenario A: Network Infrastructure Breach
        if "exploit" in alert_text.lower() or "fraud" in alert_text.lower():
            solution_metadata = {
                "source_vulnerability": alert_text,
                "framework_assignment": "cPHulk-CIST / Layer-7 ModSecurity Engine",
                "remediation_protocol": "Deploy multi-factor authentication layer filters to lock down affected subnets.",
                "joomla_category_id": 101  # Cybersecurity Index
            }
            
        # Scenario B: Environmental Hazard / Infrastructure Failure
        elif "hurricane" in alert_text.lower() or "safety" in alert_text.lower():
            solution_metadata = {
                "source_vulnerability": alert_text,
                "framework_assignment": "Environment-Safety-Monitor (Deterministic C++)",
                "remediation_protocol": "Initialize multi-core real-time hardware telemetry bridges to stabilize logistics.",
                "joomla_category_id": 102  # Infrastructure Logistics
            }
            
        # Scenario C: Bio-Containment / Public Health Risk
        elif "infestation" in alert_text.lower() or "contamination" in alert_text.lower():
            solution_metadata = {
                "source_vulnerability": alert_text,
                "framework_assignment": "VirusTC / Material Disposition Log Matrix",
                "remediation_protocol": "Trigger automated remote triage tracking protocols and cold-chain integrity assurance.",
                "joomla_category_id": 103  # Biosecurity & Public Health
            }

        if solution_metadata:
            self._write_outputs(threat_source, solution_metadata)

    def _write_outputs(self, title: str, metadata: dict):
        """
        Compiles the solution data into Markdown, PDF parameters, and Joomla payloads.
        """
        safe_title = title.lower().replace(" ", "_")
        
        # 1. Output clean Markdown Solution Report
        md_path = REPORTS_DIR / f"solution_{safe_title}.md"
        md_content = f"""# Engineering Action Report: {title}
## Threat Assessment
{metadata['source_vulnerability']}

## Resolution Infrastructure
**Assigned Subsystem:** {metadata['framework_assignment']}
**Remediation Steps:** {metadata['remediation_protocol']}

*Sourced via https://gundam.solutions and official military-technical manuals.*
"""
        md_path.write_text(md_content)
        
        # 2. Output Joomla 6 Web Services API Compliant JSON Article Payload
        joomla_path = API_DIR / f"joomla_{safe_title}.json"
        joomla_payload = {
            "title": f"Defense Solution: {title}",
            "catid": metadata['joomla_category_id'],
            "articletext": f"<h1>{title} Resolved</h1><p>{metadata['remediation_protocol']}</p>",
            "state": 1,
            "language": "*"
        }
        
        with open(joomla_path, 'w', encoding='utf-8') as f:
            json.dump(joomla_payload, f, indent=4)

        print(f"🌟 Engineered Solution compiled for: {title}")
