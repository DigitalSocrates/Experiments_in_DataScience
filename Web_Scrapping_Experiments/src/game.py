""" represents each game"""
import pandas as pd
import numpy

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


    def set_game_date (self, game_date):
        """ set game date """
        if self.debug:
            print(game_date)
        self.game_date = game_date


    def set_numbers (self, lis):
        """ set all numbers from a provided list """
        position = 1
        for li_cell in lis:
            if self.debug:
                print(li_cell)
            if position == 1:
                self.set_first_ball(li_cell.text.strip())
            elif position == 2:
                self.set_second_ball(li_cell.text.strip())
            elif position == 3:
                self.set_third_ball(li_cell.text.strip())
            elif position == 4:
                self.set_forth_ball(li_cell.text.strip())
            elif position == 5:
                self.set_fifth_ball(li_cell.text.strip())
            elif position == 6:
                self.set_power_ball(li_cell.text.strip())
            position += 1


    # Setter methods
    def set_first_ball(self, ball : int):
        """ set first ball """
        self.first_ball = ball


    def set_second_ball(self, ball : int):
        """ set second ball """
        self.second_ball = ball


    def set_third_ball(self, ball : int):
        """ set third ball """
        self.third_ball = ball


    def set_fourth_ball(self, ball : int):
        """ set fourth ball """
        self.fourth_ball = ball


    def set_fifth_ball(self, ball : int):
        """ set fifth ball """
        self.fifth_ball = ball


    def set_power_ball(self, ball : int):
        """ set power ball """
        self.power_ball = ball


    def get_game_stats (self):
        """ print game statistics """
        print (f"{self.game_date},\
               {self.first_ball},\
               {self.second_ball},\
               {self.third_ball},\
               {self.fourth_ball},\
               {self.fifth_ball},\
               {self.power_ball}")


    def get_df_row(self):
        """ create a row for the dataframe """
        new_row = {'Date': self.game_date,
                'Ball_1': self.first_ball,
                'Ball_2': self.second_ball,
                'Ball_3': self.third_ball,
                'Ball_4': self.fourth_ball,
                'Ball_5': self.fifth_ball,
                'Ball_Bonus': self.power_ball,
                }

        return new_row


    def get_game_dataframe (self) -> pd.DataFrame:
        """ get game dataframe """
        dtypes = numpy.dtype(
        [
            ('Date', 'datetime64[ns]'),
            ('Ball_1', numpy.float64),
            ('Ball_2',numpy.float64),
            ('Ball_3',numpy.float64),
            ('Ball_4',numpy.float64),
            ('Ball_5',numpy.float64),
            ('Ball_Bonus',numpy.float64),
            ]
        )

        return pd.DataFrame(numpy.empty(0, dtype=dtypes))
