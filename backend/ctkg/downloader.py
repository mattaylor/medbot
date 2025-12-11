import requests
import json
import os
from typing import List, Dict

class ClinicalTrialsDownloader:
    BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
    
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def download_studies(self, limit: int = 100, query: str = None):
        params = {"pageSize": limit}
        if query:
            params["query.term"] = query
            
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        studies = data.get("studies", [])
        
        output_file = os.path.join(self.data_dir, "studies_raw.json")
        with open(output_file, "w") as f:
            json.dump(studies, f, indent=2)
            
        print(f"Downloaded {len(studies)} studies to {output_file}")
        return studies

if __name__ == "__main__":
    # Use absolute path for safety
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(base_dir, "data", "ctkg")
    downloader = ClinicalTrialsDownloader(data_dir=data_dir)
    downloader.download_studies(limit=50)
