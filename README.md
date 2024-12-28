# common-xi-scraper

This project scrapes cricket player statistics from ESPN Cricinfo for various teams over the period of 2010-2019. It fetches data on the number of matches played by each player at specific batting positions, and compiles the information to generate a "best XI" for each team based on the number of matches played at each position.

## Features

- Fetches player data for multiple cricket teams.
- Scrapes the batting statistics for each player.
- Tracks the number of matches played at each batting position.
- Builds a "best XI" for each team based on position-specific match counts.
- Exports player statistics to a CSV file.
- Supports headless operation for running without opening a visible browser window.

## Requirements

- Python 3.x
- Selenium (`pip install selenium`)
- WebDriver Manager (`pip install webdriver-manager`)
- A browser driver for Chrome (e.g., ChromeDriver)

## Setup

1. Clone the repository or download the script.
2. Install the required Python packages using pip:

    ```bash
    pip install selenium webdriver-manager
    ```

3. Make sure you have the Chrome browser installed, as the script uses ChromeDriver for web scraping.

## How It Works

- The script uses the Selenium WebDriver to navigate to ESPN Cricinfo's player and team statistics pages.
- It fetches the list of players for each team and their batting statistics from the period 2010-2019.
- The script counts the number of matches each player has played at each batting position (from 1 to 11).
- It then builds the "best XI" for each team by selecting the player with the highest number of matches played at each position.
- The data for all players is saved in a CSV file named `<team_name>_player_data.csv`.

## Teams Processed

- South Africa
- England
- New Zealand
- Australia
- India
- Pakistan
- West Indies
- Sri Lanka
- Bangladesh
- Afghanistan
- Zimbabwe

## License

This project is for educational and research purposes only. The data is scraped from ESPN Cricinfo, and proper attribution is given in the `LICENSE` file.

## Disclaimer

This script is intended for personal use only and should not be used for commercial purposes. Web scraping is subject to the terms of service of the website being scraped, and it is advised to review those terms before using this script.





