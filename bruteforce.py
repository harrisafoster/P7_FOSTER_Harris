import pandas as pd


class BruteForce:
    def __init__(self, datasheet, budget=500):
        self.df = pd.read_csv(datasheet)
        self.budget = budget

    def sort_and_add_earnings(self):
        sorted_df = self.df.sort_values(by=['profit'], ascending=False)
        sorted_df['amount_earned'] = sorted_df['price'] * sorted_df['profit']
        return sorted_df

    def make_items(self):
        list_of_items = []
        for index, row in self.sort_and_add_earnings().iterrows():
            new_item = {'name': row['name'], 'price': row['price'], 'amount_earned': row['amount_earned'] / 100}
            list_of_items.append(new_item)
        return list_of_items

    def determine_optimal_investments(self, df):
        price = df['price']
        amount_earned = df['amount_earned']
        n = len(amount_earned)
        prices = []
        amounts_earned = []

        K = [[0 for x in range(self.budget + 1)] for x in range(n + 1)]

        for i in range(n + 1):
            for w in range(self.budget + 1):
                if i == 0 or w == 0:
                    K[i][w] = 0
                elif price[i - 1] <= w:
                    K[i][w] = max(amount_earned[i - 1] + K[i - 1][w - price[i - 1]], K[i - 1][w])
                else:
                    K[i][w] = K[i - 1][w]

        res = K[n][self.budget]
        w = self.budget
        for i in range(n, 0, -1):
            if res <= 0:
                break
            if res == K[i - 1][w]:
                continue
            else:
                prices.append(price[i - 1])
                amounts_earned.append(amount_earned[i - 1] / 100)
                res = res - amount_earned[i - 1]
                w = w - price[i - 1]
        final_items = []
        associated_prices = []
        for i in range(len(prices[:-1])):
            associated_prices.append([prices[i], amounts_earned[i]])
        for item in self.make_items():
            if [item['price'], item['amount_earned']] in associated_prices:
                final_items.append(item)
        return sum(prices), K[n][self.budget] / 100, final_items


obj_bruteforce = BruteForce('datasets/sheet1.csv')

print(obj_bruteforce.determine_optimal_investments(obj_bruteforce.sort_and_add_earnings()))
