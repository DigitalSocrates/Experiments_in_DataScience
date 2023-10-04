""" Utility File Primarily for Convenience """
import os
from datetime import datetime
from itertools import permutations
import pandas as pd
import requests
from bs4 import BeautifulSoup
from src.game import Game


def scrape_lottery_data(year: int, file_path: str,
                        date_format: str,
                        save_as: str = 'parquet'):
    """
    Scrape Lottery Website by Year

    This function scrapes data from a lottery website, with the option 
    to save the data for each year in separate files. 
    
    By default, the data is saved in the Parquet format, 
    but you can specify CSV format if desired.

    Args:
        year (int): The year for which to scrape lottery data.
        file_path (str): The path where the scraped data will be saved.
        date_format (str): The format of the date in the scraped data.
        save_as (str, optional): The format to save the data
            (either 'parquet' or 'csv'). Defaults to 'parquet'.
    """

    # instantiate game object
    game = Game()

    # get a new game dataframe
    games_df = game.create_empty_game_dataframe()

    # URL for Powerball past drawings
    url = "https://www.walottery.com/WinningNumbers/PastDrawings.aspx?" +\
        f"gamename=powerball&unittype=year&unitcount={year}"

    try:
        # Send an HTTP GET request
        response = requests.get(url, timeout=60)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print(f'Error: Could not get URL {url} due to a timeout.')
        return
    except requests.exceptions.RequestException as ex:
        print(f'Error: An error occurred while fetching the data: {str(ex)}')
        return

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table containing the data
    all_numbers = soup.find_all('table', class_='table-viewport-small')

    game_data = []

    # Iterate through rows in the table to extract data
    for numbers in all_numbers:
        # Set date of the game
        game.set_game_date(
            datetime.strptime(
                numbers.find('thead').h2.text.strip(), date_format))
        # Set balls
        td_cell = numbers.find('td', class_='game-balls')
        game.set_numbers(td_cell.find('ul').find_all('li'))
        # Append game results to list
        game_data.append(game.create_dataframe_row())

    if game_data:
        # Create a DataFrame from the list of game data
        games_df = pd.DataFrame(game_data)

        # Define the output file path
        output_file_path = os.path.join(file_path, f"powerball_{year}")

        if save_as == "parquet":
            # Save the DataFrame as a Parquet file
            games_df.to_parquet(f"{output_file_path}.parquet", index=False)
        else:
            # Save the DataFrame as a CSV file
            games_df.to_csv(f"{output_file_path}.csv", index=False)
    else:
        print(f"No game data found for {year}.")


def read_all_parquet_files(directory: str):
    """
    Merge all Parquet files in a directory into a single DataFrame.

    Args:
        directory (str): The directory containing Parquet files.

    Returns:
        pd.DataFrame or None: A concatenated DataFrame of Parquet files or None if there are issues.
    """
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return None

    parquet_files = [file for file in os.listdir(directory)
                     if file.endswith(".parquet")]

    if not parquet_files:
        print(f"Error: No .parquet files found in directory '{directory}'.")
        return None

    dfs = [pd.read_parquet(os.path.join(directory, file)) for file in parquet_files]

    if dfs:
        return pd.concat(dfs, ignore_index=True)

    return None


def generate_value_permutations(p, q, d):
    """ generate all permutations based on your input """
    values = (p, q, d)
    # Generate all permutations
    permuted_values = permutations(values)

    # Iterate through and print the permutations in the desired format
    for perm in permuted_values:
        print(f'({", ".join(perm)})')


if __name__ == '__main__':
    scrape_lottery_data(year=2023, file_path='./',
                        date_format='%a, %b %d, %Y',
                        save_as='csv')
