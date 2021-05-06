import pandas as pd
import numpy as np


class BruteForce:
    def __init__(self, datasheet):
        self.df = pd.read_csv(datasheet)
        self.budget = 500
        self.spent = 0
        self.earned = 0
        self.stocks_to_buy = []

    def sort_and_add_earnings(self):
        sorted_df = self.df.sort_values(by=['profit'], ascending=False)
        sorted_df['amount_earned'] = sorted_df['price'] * sorted_df['profit']
        return sorted_df

    def determine_optimal_investments(self):
        for index, row in self.sort_and_add_earnings().iterrows():
            if self.spent < 500 and (self.spent + row['price']) <= 500:
                self.spent += row['price']
                self.earned += row['amount_earned']
                self.stocks_to_buy.append(row['name'])
        return self.spent, self.earned, self.stocks_to_buy


obj_bruteforce = BruteForce('sheet1.csv')

print(obj_bruteforce.determine_optimal_investments())