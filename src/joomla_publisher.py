import os
import json
import requests
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
API_PAYLOAD_DIR = ROOT_DIR / "docs" / "reports" / "API"

class JoomlaPublisher:
    """
    Direct web-services integration client for Joomla 6 Core API.
    Pushes completed think tank reports straight to targeted category trees.
    """
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip('/')
        # Joomla 6 mandates a Bearer token generated via User Manager
        self.headers = {
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/json",
            "X-Joomla-Token": api_token  # Core authentication header
        }

    def publish_pending_reports(self):
        """
        Iterates over the docs/reports/API directory and distributes JSON objects
        to your live web endpoints.
        """
        if not API_PAYLOAD_DIR.exists():
            print("API cache directory not initialized yet.")
            return

        json_payloads = list(API_PAYLOAD_DIR.glob("*.json"))
        if not json_payloads:
            print("No pending articles ready for Joomla ingestion.")
            return

        for path in json_payloads:
            print(f"Found payload: {path.name}")
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    payload_data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Malformed JSON syntax inside: {path.name}")
                    continue
            
            self._execute_post(path, payload_data)

    def _execute_post(self, file_path: Path, data: dict):
        """
        Executes HTTP POST request to your core content delivery network partition.
        """
        endpoint = f"{self.base_url}/api/v1/content/articles" # Joomla 6 default Web Services path
        
        try:
            # Pushing clean article text mapping natively into Joomla database parameters
            response = requests.post(endpoint, json=data, headers=self.headers, timeout=15)
            
            if response.status_code in [200, 201]:
                print(f"Successfully published to Joomla! Asset: {data.get('title')}")
                # Safe-delete or archive payload once successfully live on the server
                file_path.unlink()
            else:
                print(f"Ingestion Refused ({response.status_code}): {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"Network layer fault encountered during transmission: {e}")
