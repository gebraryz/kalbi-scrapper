import json
import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from tqdm import tqdm

KALBI_URL = "https://www.kalbi.pl"
CURRENT_YEAR = datetime.now().year
FILENAME = f"swieta_{CURRENT_YEAR}.json"
ICS_FILENAME = f"swieta_{CURRENT_YEAR}.ics"


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


def scrape_website():
    start_date = datetime(CURRENT_YEAR, 1, 1)
    end_date = datetime(CURRENT_YEAR, 12, 31)

    holidays = []

    for i in tqdm(range((end_date - start_date).days + 1), desc=f"Scraping Kalbi {CURRENT_YEAR}"):
        date_with_year = start_date + timedelta(days=i)

        splitted_date_with_year = str(date_with_year).split("-")
        date_without_year = (
            f"{splitted_date_with_year[1]}/{splitted_date_with_year[2].split(" ")[0]}"
        )

        month = MONTHS[date_with_year.month]

        day_url = f"{KALBI_URL}/{date_with_year.day}-{month}"

        response = requests.get(f"{KALBI_URL}/{date_with_year.day}-{month}")
        if response.status_code != 200:
            print(f"Błąd pobierania: {day_url}")

        soup = BeautifulSoup(response.text, "html.parser")

        holidays_section = soup.find("section", class_="calCard-ententa")

        holidays.append(
            {
                "date": date_without_year,
                "holidays": (
                    [re.sub(r"[^\w\s]", "", a.text.strip()) for a in holidays_section.find_all("a")]
                    if holidays_section
                    else []
                ),
            }
        )

    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(holidays, f, indent=4, ensure_ascii=False)

    print(f"Zapisano święta do {FILENAME}")


def generate_ics_file():
    with open(FILENAME, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    calendar = Calendar()

    for day in json_data:
        date_str = day["date"].replace("\xa0", " ").strip()

        try:
            date = datetime.strptime(date_str, "%m/%d")
        except ValueError:
            print(f"Błąd parsowania daty: {date_str}")
            continue

        date = date.replace(year=CURRENT_YEAR)

        for holiday in day["holidays"]:
            event = Event()
            event.name = holiday
            event.begin = date 
            event.end = event.begin
            event.description = holiday
            event.location = "Polska"

            event.make_all_day()
            event.rrule = {
                "freq": "yearly",
                "count": 100,
            } 

            calendar.events.add(event)

    with open(ICS_FILENAME, "w", encoding="utf-8") as f:
        f.writelines(calendar)

    print(f"Plik .ics został zapisany jako {ICS_FILENAME}")


scrape_website()
generate_ics_file()
