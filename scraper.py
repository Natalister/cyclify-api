import requests
from bs4 import BeautifulSoup
from datetime import datetime

def country_code_to_flag(country_code: str) -> str:
    if not country_code or len(country_code) != 2:
        return "🏁"
    return "".join(chr(0x1F1E6 + ord(c) - ord('A')) for c in country_code.upper())

def parse_date(d, year):
    return datetime.strptime(f"{d}.{year}", "%d.%m.%Y").date()

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
        table = tables[1]

        races = []

        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue

            try:
                category = cols[3].get_text(strip=True)
                if "UWT" not in category:
                    continue

                date_text = cols[0].get_text(strip=True).replace(" ", "")
                parts = date_text.split("-")
                start_str = parts[0].strip()
                end_str = parts[1].strip() if len(parts) > 1 else None

                start = parse_date(start_str, year)
                end = parse_date(end_str, year) if end_str else None

                if start < today:
                    continue

                name_tag = cols[1].find("a")
                name = name_tag.get_text(strip=True) if name_tag else cols[1].get_text(strip=True)

                flag_span = cols[1].find("span", class_="flag")
                country_code = ""
                if flag_span:
                    classes = flag_span.get("class", [])
                    country_code = next((c.replace("flag-", "") for c in classes if c.startswith("flag-")), "")

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
