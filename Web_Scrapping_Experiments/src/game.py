"""
Represents an Instance of a Lottery Game

This class serves as a fundamental data structure to represent individual
lottery games. It collects and stores crucial information about each game,
including details such as the drawn balls and the date on which the
game took place."""
import pandas as pd
import numpy as np


class Game:
    """ contans date of the game and all the balls """
    debug = False

    def __init__(self):
        self.game_date: None
        self.first_ball: None
        self.second_ball: None
        self.third_ball: None
        self.fourth_ball: None
        self.fifth_ball: None
        self.power_ball: None

    def set_game_date(self, game_date):
        """
        Set the game date attribute.

        Args:
            game_date (str): The game date to be set.

        Returns:
            None
        """
        if self.debug:
            print(game_date)
        self.game_date = game_date

    def set_numbers(self, lis):
        """Set numbers from a provided list.

        Args:
            lis (list): A list containing numbers.

        Returns:
            None
        """
        for position, number in enumerate(lis, start=1):
            if self.debug:
                print(number)

            if position == 1:
                self.set_first_ball(number.text.strip())
            elif position == 2:
                self.set_second_ball(number.text.strip())
            elif position == 3:
                self.set_third_ball(number.text.strip())
            elif position == 4:
                self.set_fourth_ball(number.text.strip())
            elif position == 5:
                self.set_fifth_ball(number.text.strip())
            elif position == 6:
                self.set_power_ball(number.text.strip())

    # Setter methods
    def set_first_ball(self, ball: int):
        """ set first ball """
        self.first_ball = ball

    def set_second_ball(self, ball: int):
        """ set second ball """
        self.second_ball = ball

    def set_third_ball(self, ball: int):
        """ set third ball """
        self.third_ball = ball

    def set_fourth_ball(self, ball: int):
        """ set fourth ball """
        self.fourth_ball = ball

    def set_fifth_ball(self, ball: int):
        """ set fifth ball """
        self.fifth_ball = ball

    def set_power_ball(self, ball: int):
        """ set power ball """
        self.power_ball = ball

    def get_game_stats(self):
        """ print game statistics """
        print(f"{self.game_date},\
               {self.first_ball},\
               {self.second_ball},\
               {self.third_ball},\
               {self.fourth_ball},\
               {self.fifth_ball},\
               {self.power_ball}")

    def create_dataframe_row(self):
        """
        Create a row dictionary for a DataFrame.

        Returns:
            dict: A dictionary containing the column names as keys and corresponding values.
        """
        new_row = {
            'Date': self.game_date,
            'Ball_1': self.first_ball,
            'Ball_2': self.second_ball,
            'Ball_3': self.third_ball,
            'Ball_4': self.fourth_ball,
            'Ball_5': self.fifth_ball,
            'Ball_Bonus': self.power_ball,
            }
        return new_row

    def create_empty_game_dataframe(self) -> pd.DataFrame:
        """
        Create an empty DataFrame to represent lottery game data.

        Returns:
            pd.DataFrame: An empty DataFrame with predefined columns.
        """
        column_data_types = np.dtype([
            ('Date', 'datetime64[ns]'),
            ('Ball_1', np.float64),
            ('Ball_2', np.float64),
            ('Ball_3', np.float64),
            ('Ball_4', np.float64),
            ('Ball_5', np.float64),
            ('Ball_Bonus', np.float64),
            ])

        # Create an empty DataFrame with the specified column data types
        empty_dataframe = pd.DataFrame(np.empty(0, dtype=column_data_types))

        return empty_dataframe
