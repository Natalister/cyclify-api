import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

def get_upcoming_races():
    url = "https://www.procyclingstats.com/races.php?year=2025&circuit=1&class=2.UWT"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        races = []
        table = soup.find("table")
        
        if not table:
            return {"error": "table not found", "races": []}
        
        rows = table.find_all("tr")[1:]  # skip header
        
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue
            
            try:
                date_text = cols[0].get_text(strip=True)
                name = cols[2].get_text(strip=True)
                country = cols[1].find("span", class_="flag")
                country_code = country["class"][1] if country else ""
                
                # Garder seulement les courses futures
                races.append({
                    "name": name,
                    "date": date_text,
                    "country": country_code,
                })
            except Exception:
                continue
        
        return {"races": races, "updated_at": datetime.utcnow().isoformat()}
    
    except Exception as e:
        return {"error": str(e), "races": []}
