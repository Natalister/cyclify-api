import requests
from datetime import datetime

def get_upcoming_races():
    year = datetime.now().year
    url = f"https://firstcycling.com/race.php?y={year}&t=1"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return {
            "status_code": response.status_code,
            "page_title": response.text[200:400],  # extrait un bout du HTML
            "blocked": "Just a moment" in response.text or "cloudflare" in response.text.lower()
        }
    except Exception as e:
        return {"error": str(e)}
