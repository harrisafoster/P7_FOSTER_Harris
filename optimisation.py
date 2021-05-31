import pandas as pd


class Optimisation:
    def __init__(self, datasheet, budget=500):
        self.df = pd.read_csv(datasheet)
        self.budget = budget

    def filter_data(self):
        filtered_df = self.df.query('price > 0')
        filtered_df = filtered_df.reset_index(drop=True)
        return filtered_df

    def add_profit_column(self):
        df = self.filter_data()
        sorted_df = df.sort_values(by=['profit'], ascending=False)
        sorted_df['amount_earned'] = sorted_df['price'] * (sorted_df['profit'] / 100)
        return sorted_df

    def make_item_list(self):
        list_of_items = []
        for index, row in self.add_profit_column().iterrows():
            new_item = {'name': row['name'], 'price': row['price'], 'amount_earned': row['amount_earned']}
            list_of_items.append(new_item)
        return list_of_items

    def determine_optimal_investments(self, df):
        amount_earned = df['amount_earned'].to_list()
        price = df['price'].to_list()
        rounded_multiplied_budget = self.budget * 100  # rmb
        index = len(amount_earned)

        combination_matrix = [[-1 for i in range(rounded_multiplied_budget + 1)] for j in range(index + 1)]

        def check_all_combinations(internal_price, internal_earned, internal_rmb, internal_index):
            if internal_index == 0 or internal_rmb == 0:
                return 0
            if combination_matrix[internal_index][internal_rmb] != -1:
                return combination_matrix[internal_index][internal_rmb]
            if (int(internal_price[internal_index - 1] * 100)) <= internal_rmb:
                combination_matrix[internal_index][internal_rmb] = max(
                    internal_earned[internal_index - 1] + check_all_combinations(
                        internal_price, internal_earned,
                        internal_rmb - (int(internal_price[internal_index - 1] * 100)),
                        internal_index - 1),
                    check_all_combinations(internal_price, internal_earned, internal_rmb, internal_index - 1))
                return combination_matrix[internal_index][internal_rmb]
            elif (int(internal_price[internal_index - 1] * 100)) > internal_rmb:
                combination_matrix[internal_index][internal_rmb] = check_all_combinations(internal_price,
                                                                                          internal_earned,
                                                                                          internal_rmb,
                                                                                          internal_index - 1)
                return combination_matrix[internal_index][internal_rmb]

        final_result = check_all_combinations(price, amount_earned, rounded_multiplied_budget, index)
        rmb = rounded_multiplied_budget
        prices = []
        amounts_earned = []
        for i in range(index, 0, -1):
            if final_result <= 0:
                break
            if final_result == combination_matrix[i - 1][rmb]:
                continue
            elif rmb - int(price[i - 1] * 100) >= 0:
                prices.append(price[i - 1])
                amounts_earned.append(amount_earned[i - 1])
                final_result = final_result - amount_earned[i - 1]
                rmb = rmb - int(price[i - 1] * 100)
        final_items = []
        associated_prices = []
        for i in range(len(prices)):
            associated_prices.append([prices[i], amounts_earned[i]])
        for item in self.make_item_list():
            if [item['price'], item['amount_earned']] in associated_prices:
                final_items.append(item)
        return sum(prices), sum(amounts_earned), final_items


test_20 = Optimisation('datasets/sheet1.csv')
test_dataset1 = Optimisation('datasets/dataset1.csv')
test_dataset2 = Optimisation('datasets/dataset2.csv')
test_dataset1_sample = Optimisation('datasets/dataset1_sample.csv')
test_dataset2_sample = Optimisation('datasets/dataset2_sample.csv')

print(test_20.determine_optimal_investments(test_20.add_profit_column()))
print(test_dataset1_sample.determine_optimal_investments(test_dataset1_sample.add_profit_column()))
# print(test_dataset1.determine_optimal_investments(test_dataset1.add_profit_column()))
# print(test_dataset2.determine_optimal_investments(test_dataset2.add_profit_column()))
