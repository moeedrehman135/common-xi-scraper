from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from collections import defaultdict
import csv

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run without opening a visible browser window
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Define the base URL for team player statistics
team_url = (
    "https://stats.espncricinfo.com/ci/engine/stats/index.html?"
    "class=3;filter=advanced;orderby=matches;size=200;"
    "spanmax1=31+Dec+2019;spanmax2=31+Dec+2019;spanmin1=01+Jan+2010;spanmin2=01+Jan+2010;"
    "spanval1=span;spanval2=span;team={team_id};template=results;type=batting"
)

# Define the base URL for individual player statistics
player_base_url = (
    "https://stats.espncricinfo.com/ci/engine/player/{player_id}.html?"
    "class=3;spanmax1=31+Dec+2019;spanmax2=31+Dec+2019;"
    "spanmin1=01+Jan+2010;spanmin2=01+Jan+2010;spanval1=span;spanval2=span;"
    "team={team_id};template=results;type=batting;view=innings"
)

def fetch_players(team_id):
    """Fetches the list of players who played for the team during 2010-2019."""
    url = team_url.format(team_id=team_id)
    driver.get(url)
    
    # Wait for the player table to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "engineTable")))
    
    # Find player rows
    rows = driver.find_elements(By.CSS_SELECTOR, ".engineTable .data1")
    players = []
    
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        if not columns:
            continue
        
        # Extract player name and player ID
        player_name = columns[0].text.strip()
        player_link = columns[0].find_element(By.TAG_NAME, "a").get_attribute("href")
        player_id = player_link.split("/")[-1].split(".")[0]  # Extract player ID from the URL
        
        # Ensure valid data and add to the list
        if player_name and player_id:
            players.append((player_name, player_id))
    
    return players

def fetch_position_stats(player_id, team_id):
    """Fetch the number of matches played at each position by a player."""
    url = player_base_url.format(player_id=player_id, team_id=team_id)
    driver.get(url)
    
    # Wait for the innings stats table to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "engineTable")))
    
    # Find the innings rows in the table
    rows = driver.find_elements(By.CSS_SELECTOR, ".engineTable .data1")
    position_counts = defaultdict(int)
    
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        if not columns:
            continue
        
        # Extract batting position
        try:
            position = int(columns[6].text.strip())  # 'Pos' column
            if 1 <= position <= 11:  # Ensure the position is valid
                position_counts[position] += 1
        except ValueError:
            continue  # Skip invalid entries
    
    return position_counts

def build_best_xi_for_team(team_id, team_name):
    """Build the best XI for a team based on the most matches played at each position."""
    players = fetch_players(team_id)
    print(f"Fetched {len(players)} players for team ID {team_id}")
    
    best_xi = {pos: {"player": "", "matches": 0} for pos in range(1, 12)}
    all_player_data = []  # List to store data for all players
    
    for player_name, player_id in players:
        print(f"Processing {player_name}...")
        position_stats = fetch_position_stats(player_id, team_id)
        
        # Save player data
        for pos, matches in position_stats.items():
            all_player_data.append({
                "Team": team_name,
                "Player": player_name,
                "Position": pos,
                "Matches": matches
            })
        
        # Update best XI
        for pos, matches in position_stats.items():
            if matches > best_xi[pos]["matches"]:
                best_xi[pos]["player"] = player_name
                best_xi[pos]["matches"] = matches
    
    # Write all player data to a CSV file
    with open(f"{team_name}_player_data.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Team", "Player", "Position", "Matches"])
        writer.writeheader()
        writer.writerows(all_player_data)
    
    return best_xi

# Define team ID mappings
teams = {
    "South Africa": 3,
    "England": 1,
    "New Zealand": 5,
    "Australia": 2,
    "India": 6,
    "Pakistan": 7,
    "West Indies": 4,
    "Sri Lanka": 8,
    "Bangladesh": 25,
    "Afghanistan": 40,
    "Zimbabwe": 9
}

# Collect data for all teams
for team, team_id in teams.items():
    print(f"\nBuilding best XI for {team}...")
    try:
        best_xi = build_best_xi_for_team(team_id, team)
        print(f"Best XI for {team}:")
        for pos, data in best_xi.items():
            print(f"Position {pos}: {data['player']} ({data['matches']} matches)")
    except Exception as e:
        print(f"An error occurred while processing {team}: {e}")

# Close the driver after fetching all data
driver.quit()
