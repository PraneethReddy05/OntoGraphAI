# backend/services/openalex_service.py
import requests

class OpenAlexService:
    BASE_URL = "https://api.openalex.org/works"

    def get_paper_by_doi(self, doi):
        url = f"{self.BASE_URL}/doi:{doi}"
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None

    def get_paper_by_id(self, work_id):
        url = f"{self.BASE_URL}/{work_id}"
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None

    def search_papers_by_topic(self, topic, limit=1):
        url = f"{self.BASE_URL}?search={topic}&per-page={limit}"
        r = requests.get(url)
        return r.json().get("results", []) if r.status_code == 200 else []
