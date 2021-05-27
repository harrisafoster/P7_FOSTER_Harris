import pandas as pd


class Optimisation:
    def __init__(self, datasheet, budget=500):
        self.df = pd.read_csv(datasheet)
        self.budget = budget

    def filter_data(self):
        filtered_df = self.df.query('price > 0')
        filtered_df = filtered_df.reset_index(drop=True)
        return filtered_df

    def sort_data(self):
        df = self.filter_data()
        sorted_df = df.sort_values(by=['profit'], ascending=False)
        sorted_df['amount_earned'] = sorted_df['price'] * (sorted_df['profit'] / 100)
        return sorted_df

    def make_items(self):
        list_of_items = []
        for index, row in self.sort_data().iterrows():
            new_item = {'name': row['name'], 'price': row['price'], 'amount_earned': row['amount_earned']}
            list_of_items.append(new_item)
        return list_of_items

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

    def determine_optimal_investments(self, df):
        amount_earned = df['amount_earned']  # val
        price = df['price']  # wt
        capacity = self.budget * 100  # W
        n = len(amount_earned)

        knapsack_matrix = [[-1 for i in range(capacity + 1)] for j in range(n + 1)]

        def recursive_knapsack(wt, val, W, n):
            if n == 0 or W == 0:
                return 0
            if knapsack_matrix[n][W] != -1:
                return knapsack_matrix[n][W]
            if (int(wt[n - 1] * 100)) <= W:
                #TODO find a way to store chosen values here?
                knapsack_matrix[n][W] = max(
                    val[n - 1] + recursive_knapsack(
                        wt, val, W - (int(wt[n - 1] * 100)), n - 1),
                    recursive_knapsack(wt, val, W, n - 1))
                return knapsack_matrix[n][W]
            elif (int(wt[n - 1] * 100)) > W:
                knapsack_matrix[n][W] = recursive_knapsack(wt, val, W, n - 1)
                return knapsack_matrix[n][W]

        res = recursive_knapsack(price, amount_earned, capacity, n)
        print(res)
        w = capacity
        prices = []
        amounts_earned = []
        #TODO problem is here in the way it finds data.
        for i in range(n, 0, -1):
            if res <= 0:
                break
            if res == knapsack_matrix[i - 1][w]:
                continue
            elif w - int(price[i - 1] * 100) >= 0:
                prices.append(price[i - 1])
                amounts_earned.append(amount_earned[i - 1])
                res = res - amount_earned[i - 1]
                w = w - int(price[i - 1] * 100)
        final_items = []
        associated_prices = []
        for i in range(len(prices)):
            associated_prices.append([prices[i], amounts_earned[i]])
        for item in self.make_items():
            if [item['price'], item['amount_earned']] in associated_prices:
                final_items.append(item)
        return sum(prices), sum(amounts_earned), final_items


test_20 = Optimisation('datasets/sheet1.csv')
test_dataset1 = Optimisation('datasets/dataset1.csv')
test_dataset2 = Optimisation('datasets/dataset2.csv')
test_dataset1_sample = Optimisation('datasets/dataset1_sample.csv')
test_dataset2_sample = Optimisation('datasets/dataset2_sample.csv')

print(test_20.determine_optimal_investments(test_20.sort_data()))
#print(test_dataset1_sample.determine_optimal_investments(test_dataset1_sample.sort_data()))
#print(test_dataset1.determine_optimal_investments((test_dataset1.sort_data())))
