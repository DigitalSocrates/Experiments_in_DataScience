""" utility file mostly for convinience """
import os
import requests
import pandas as pd
from itertools import permutations
from datetime import datetime
from bs4 import BeautifulSoup
from src.game import Game

def scrape_lottery_data(year : int, file_path : str, date_format : str, save_as : str = 'parquet'):
    """ scrape lottery web site by year
        store each years data in a separate file 
        default format is parquet otherwise the dataset will be saved in csv format
    """
    # instantiate game object
    game = Game()

    # get a new game dataframe
    games_df = game.get_game_dataframe()

    # URL for Powerball past drawings
    url = f"https://www.walottery.com/WinningNumbers/PastDrawings.aspx?gamename=powerball&unittype=year&unitcount={year}"

    # Send an HTTP GET request
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table containing the data
    all_numbers = soup.find_all('table', class_='table-viewport-small')

    # Iterate through rows in the table to extract data
    for numbers in all_numbers:
        # set date of the game
        game.set_game_date(datetime.strptime(numbers.find('thead').h2.text.strip(), date_format))
        # set balls
        td = numbers.find('td', class_='game-balls')
        game.set_numbers(td.find('ul').find_all('li'))
        # add game results to dataframe
        games_df = pd.concat([games_df, pd.DataFrame.from_records([game.get_df_row()])])

    # check the format to save the data as 
    if save_as == "parquet":
        # Save the DataFrame as a Parquet file
        games_df.to_parquet(f"{file_path}powerball_{year}.parquet", index=False)
    else:
        games_df.to_csv(f"{file_path}powerball_{year}.csv", index=False)


def read_all_parquet_files(directory : str):
    """ combine all parquet files """
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return None

    parquet_files = [file for file in os.listdir(directory) if file.endswith(".parquet")]

    if not parquet_files:
        print(f"No .parquet files found in directory '{directory}'.")
        return None

    dfs = []
    for parquet_file in parquet_files:
        file_path = os.path.join(directory, parquet_file)
        df = pd.read_parquet(file_path)
        dfs.append(df)

    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return None


def generate_value_permutations(values = ('p', 'q', 'd')):
    """ generate all permutations based on your input """
    # Generate all permutations
    permuted_values = permutations(values)

    # Iterate through and print the permutations in the desired format
    for perm in permuted_values:
        print(f'({", ".join(perm)})')


if __name__ == '__main__':
    scrape_lottery_data(year=2023, file_path='./', date_format='%a, %b %d, %Y', save_as='csv')
