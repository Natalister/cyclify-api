import requests
from bs4 import BeautifulSoup
from datetime import datetime

def country_code_to_flag(country_code: str) -> str:
    """Convertit un code ISO 2 lettres en emoji drapeau, sans liste hardcodée."""
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

        races = []
        table = soup.find("table")

        if not table:
            return {"error": "table not found", "races": [], "html_snippet": response.text[500:1000]}

        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue

            try:
                # Dates : format "01.01 - 05.01" ou "01.01"
                date_text = cols[0].get_text(strip=True)
                parts = date_text.split("-")
                start_str = parts[0].strip()  # ex: "01.01"
                end_str = parts[1].strip() if len(parts) > 1 else None

                def parse_date(d):
                    return datetime.strptime(f"{d}.{year}", "%d.%m.%Y").date()

                start = parse_date(start_str)
                end = parse_date(end_str) if end_str else None

                # Filtre courses futures uniquement
                if start < today:
                    continue

                # Nom de la course
                name_tag = cols[2].find("a")
                name = name_tag.get_text(strip=True) if name_tag else cols[2].get_text(strip=True)

                # Pays via le drapeau img (class="flag XY")
                flag_tag = cols[1].find("span") or cols[1].find("img")
                country_code = ""
                if flag_tag:
                    classes = flag_tag.get("class", [])
                    # La classe du drapeau contient le code pays ex: ["flag", "FR"]
                    country_code = next((c for c in classes if c != "flag" and len(c) == 2), "")

                races.append({
                    "name": name,
                    "start_date": start.strftime("%-d %b"),
                    "end_date": end.strftime("%-d %b") if end else None,
                    "country": country_code_to_flag(country_code),
                    "sort_date": start.isoformat(),
                })

            except Exception:
                continue

        races.sort(key=lambda x: x["sort_date"])
        return {"races": races, "updated_at": datetime.utcnow().isoformat()}

    except Exception as e:
        return {"error": str(e), "races": []}
