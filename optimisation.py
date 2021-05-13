import pandas as pd


class Optimisation:
    def __init__(self, datasheet):
        self.df = pd.read_csv(datasheet)
        self.budget = 500

    def filter_data(self):
        filtered_df = self.df.query('price > 0')
        filtered_df = filtered_df.reset_index(drop=True)
        return filtered_df

    def sort_data(self):
        df = self.filter_data()
        sorted_df = df.sort_values(by=['profit'], ascending=False)
        sorted_df['amount_earned'] = sorted_df['price'] * (sorted_df['profit'] / 100)
        return sorted_df

    def optimise_investments(self):
        spent = 0
        earned = 0
        stocks_to_buy = []
        for index, row in self.sort_data().iterrows():
            if spent < 500 and (spent + row['price']) <= 500:
                spent += row['price']
                earned += row['amount_earned']
                stocks_to_buy.append(row['name'])
        return spent, earned, stocks_to_buy


obj_optimisation = Optimisation('datasets/dataset1.csv')
obj_optimisation2 = Optimisation('datasets/dataset2.csv')

print(obj_optimisation.optimise_investments())
print(obj_optimisation2.optimise_investments())
