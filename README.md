# Basketball Players Information Scraper
![NBA LOGO](https://pngimg.com/uploads/nba/nba_PNG14.png)
## Overview

This Python script allows you to scrape detailed information about basketball players from basketball-reference.com. It iterates through the alphabet, collecting data for players whose last names start with each letter ('a' to 'z').

## Dependencies

- Python 3.x
- Requests
- BeautifulSoup
- Pandas

## Setup

### 1. Clone the repository:

```bash
git clone https://github.com/jigsaw1313/NBA-Players-Scraper-Plus-Dataset.git
```
### 2. Navigate to the project directory:

```bash
cd basketball-players-scraper
```

### 3. Create and activate a virtual environment (Optional but recommended):

```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 5. Run the script:

```bash
python scrape_players.py
```

The script will create a CSV file named `basketball_players_data.csv` containing player information.

## Code Structure

- `scrape_players.py`: The main script for scraping player information.
- `requirements.txt`: Lists the required Python packages.

## Contribution

Contributions are welcome! If you find any issues or want to enhance the functionality, feel free to create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
