import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_upcoming_races():
    url = "https://www.procyclingstats.com/races.php?s=&year=2026&circuit=1&class=&filter=Filter"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Debug : on retourne ce qu'on trouve sur la page
        debug_info = {
            "status_code": response.status_code,
            "tables_found": len(soup.find_all("table")),
            "divs_with_class": [div.get("class") for div in soup.find_all("div")[:20]],
            "page_title": soup.title.string if soup.title else "no title",
        }
        
        return {"debug": debug_info, "races": []}
    
    except Exception as e:
        return {"error": str(e), "races": []}
