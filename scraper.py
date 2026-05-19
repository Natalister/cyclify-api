import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_upcoming_races():
    year = datetime.now().year
    url = f"https://firstcycling.com/race.php?y={year}&t=1"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    if not table:
        return {"error": "no table found"}

    # On retourne les 3 premières lignes brutes pour voir la structure
    rows = table.find_all("tr")[:4]
    debug = []
    for row in rows:
        cols = row.find_all("td")
        debug.append({
            "nb_cols": len(cols),
            "cols_text": [c.get_text(strip=True) for c in cols],
            "cols_html": [str(c)[:200] for c in cols],
        })

    return {"debug_rows": debug}
