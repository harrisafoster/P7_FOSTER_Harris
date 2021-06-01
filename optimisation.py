import pandas as pd
from os import listdir


class Optimisation:
    def __init__(self, datasheet, budget=500):
        """
        Initialisation of object
        :param datasheet: .csv format datasheet
        :param budget: by default 500, can be modified
        """
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
        """
        .make_item_list creates a list of dict values containing the names, costs, and amounts earned of all stocks
        :return: list of dict variables containing stock information
        """
        list_of_items = []
        for index, row in self.add_profit_column().iterrows():
            new_item = {'name': row['name'], 'price': row['price'], 'amount_earned': row['amount_earned']}
            list_of_items.append(new_item)
        return list_of_items

    def determine_optimal_investments(self, df):
        """
        .determine_optimal_investments tests all possible combinations of stocks to determine the optimal solution.
        :param df: Dataframe that has already been filtered and sorted goes here
        :return: total cost, total earnings, and data on the chosen stocks
        """
        amount_earned = df['amount_earned'].to_list()
        price = df['price'].to_list()
        rounded_multiplied_budget = self.budget * 100  # rmb
        index = len(amount_earned)

        combination_matrix = [[-1 for i in range(rounded_multiplied_budget + 1)] for j in range(index + 1)]

        def check_all_combinations(internal_price, internal_earned, internal_rmb, internal_index):
            """
            Dynamic function that checks all possible combinations based on given parameters
            while eliminating combinations that are redundant.
            :param internal_price: list of prices of stocks
            :param internal_earned: list of possibles earnings of stocks
            :param internal_rmb: budget multiplied by 100 and rounded in order to avoid errors resultant of FLOAT type
            variables
            :param internal_index: total amount of stocks to be examined
            :return: optimal maximum profit found in decision matrix
            """
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

        # Reconstruction of list of stocks chosen based on the amount_earned and the price constraints
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


if __name__ == "__main__":
    print('For which dataset would you like an optimised investment solution?', '\n', listdir('datasets'))
    while True:
        choice = input()
        try:
            assert choice in listdir('datasets')
        except AssertionError:
            print('Please select one of the available options.')
            continue
        else:
            break
    print("The default budget is 500€, would you like to enter a custom budget? (y/n)")
    custom_budget_choice = input()
    if custom_budget_choice == 'y':
        print("What is the client's maximum budget?")
        while True:
            budget_choice = input()
            try:
                int(budget_choice)
            except ValueError:
                print('Please enter a whole number (ex.700).')
                continue
            else:
                data_to_be_analyzed = Optimisation(('datasets/' + choice), int(budget_choice))
                print("Format: total_spent, total_earned, stocks_to_buy", '\n',
                      data_to_be_analyzed.determine_optimal_investments(data_to_be_analyzed.add_profit_column()))
                break
    if custom_budget_choice != 'y':
        data_to_be_analyzed = Optimisation(('datasets/' + choice))
        print("Format: total_spent, total_earned, stocks_to_buy", '\n',
              data_to_be_analyzed.determine_optimal_investments(data_to_be_analyzed.add_profit_column()))
