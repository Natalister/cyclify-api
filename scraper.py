import requests
from bs4 import BeautifulSoup
from datetime import datetime

def country_code_to_flag(country_code: str) -> str:
    if not country_code or len(country_code) != 2:
        return "🏁"
    return "".join(chr(0x1F1E6 + ord(c) - ord('A')) for c in country_code.upper())

def get_upcoming_races():
    year = datetime.now().year
    today = datetime.now().date()
    url = f"https://firstcycling.com/race.php?y={year}&t=1"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        tables = soup.find_all("table")
        table = tables[1]  # index 1 = table du calendrier

        races = []

        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue

            try:
                # Catégorie — on garde uniquement UWT
                category = cols[3].get_text(strip=True)
                if "UWT" not in category:
                    continue

                # Dates format "20.01-25.01" ou "20.01"
                date_text = cols[0].get_text(strip=True).replace(" ", "")
                parts = date_text.split("-")
                start_str = parts[0].strip()
                end_str = parts[1].strip() if len(parts) > 1 else None

                def parse_date(d):
                    return datetime.strptime(f"{d}.{year}", "%d.%m.%
