import json
import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from tqdm import tqdm

KALBI_URL = "https://www.kalbi.pl"
CURRENT_YEAR = datetime.now().year
FILENAME = f"holidays_{CURRENT_YEAR}.json"
ICS_FILENAME = f"holidays_{CURRENT_YEAR}.ics"

MONTHS = {
    1: "stycznia",
    2: "lutego",
    3: "marca",
    4: "kwietnia",
    5: "maja",
    6: "czerwca",
    7: "lipca",
    8: "sierpnia",
    9: "wrzesnia",
    10: "pazdziernika",
    11: "listopada",
    12: "grudnia",
}


def fetch_holidays():
    start_date = datetime(CURRENT_YEAR, 1, 1)
    end_date = datetime(CURRENT_YEAR, 12, 31)
    holidays = []

    for i in tqdm(range((end_date - start_date).days + 1), desc=f"Scraping Kalbi {CURRENT_YEAR}"):
        date_with_year = start_date + timedelta(days=i)
        date_without_year = f"{date_with_year:%m/%d}"
        month = MONTHS[date_with_year.month]
        day_url = f"{KALBI_URL}/{date_with_year.day}-{month}"

        try:
            response = requests.get(day_url, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Fetching error: {day_url} ({e})")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        holidays_section = soup.find("section", class_="calCard-ententa")

        holidays.append(
            {
                "date": f"{date_with_year:%Y-%m-%d}",
                "holidays": (
                    [re.sub(r"[^\w\s]", "", a.text.strip()) for a in holidays_section.find_all("a")]
                    if holidays_section
                    else []
                ),
            }
        )

    return holidays


def save_to_json(data):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Saved holidays to {FILENAME}")


def generate_ics_file():
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            json_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading JSON file: {e}")
        return

    calendar = Calendar()

    for day in json_data:
        try:
            date = datetime.strptime(day["date"], "%Y-%m-%d")
        except ValueError:
            print(f"Date parsing error: {day['date']}")
            continue

        for holiday in day["holidays"]:
            event = Event(name=holiday, begin=date, location="Polska")
            event.make_all_day()
            calendar.events.add(event)

    with open(ICS_FILENAME, "w", encoding="utf-8") as f:
        f.writelines(calendar)

    print(f"The .ics file has been saved as {ICS_FILENAME}")


def main():
    holidays = fetch_holidays()
    save_to_json(holidays)
    generate_ics_file()


if __name__ == "__main__":
    main()
