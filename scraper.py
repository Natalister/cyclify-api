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

    # Lister TOUTES les tables avec leur index et premier contenu
    all_tables = soup.find_all("table")
    debug = []
    for i, table in enumerate(all_tables):
        rows = table.find_all("tr")[:2]
        debug.append({
            "table_index": i,
            "table_class": table.get("class"),
            "nb_rows": len(table.find_all("tr")),
            "first_rows_text": [[c.get_text(strip=True) for c in r.find_all("td")] for r in rows],
        })

    return {"total_tables": len(all_tables), "tables": debug}
