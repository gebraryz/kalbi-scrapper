# Kalbi Scrapper

A Python script that fetches events from the [Kalbi website]("https://www.kalbi.pl/") and saves them as an `.ics` file, allowing easy calendar integration.

## Requirements

- Python 3.13+
- Poetry for dependency management

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/gebraryz/kalbi-scrapper.git
   cd kalbi-scrapper
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

## Usage

1. Run the script:

   ```bash
   poetry run python main.py
   ```

2. The script will fetch events, save them in `.json` format, and generate an `.ics` file.

## Project Structure

```
kalbi-scrapper/
│── main.py          # Main script
│── events.json      # JSON file with fetched events (generated)
│── events.ics       # ICS file with events (generated)
│── pyproject.toml   # Poetry configuration
│── README.md        # Documentation
│── LICENSE          # Project license
│── .gitignore       # Ignored files
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contribution

If you would like to contribute, feel free to open an issue or submit a pull request on GitHub. Any suggestions or improvements are welcome!
