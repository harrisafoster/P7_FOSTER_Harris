import pandas as pd
from os import listdir


class BruteForce:
    def __init__(self, datasheet, budget=500):
        """
        Initialisation of object
        :param datasheet: .csv format datasheet
        :param budget: by default 500, can be modified
        """
        self.df = pd.read_csv(datasheet)
        self.budget = budget

    def sort_and_add_earnings(self):
        sorted_df = self.df.sort_values(by=['profit'], ascending=False)
        sorted_df['amount_earned'] = sorted_df['price'] * (sorted_df['profit'] / 100)
        return sorted_df

    def make_items(self):
        """
        .make_item_list creates a list of dict values containing the names, costs, and amounts earned of all stocks
        :return: list of dict variables containing stock information
        """
        list_of_items = []
        for index, row in self.sort_and_add_earnings().iterrows():
            new_item = {'name': row['name'], 'price': row['price'], 'amount_earned': row['amount_earned']}
            list_of_items.append(new_item)
        return list_of_items

    def determine_optimal_investments(self, df):
        """
        .determine_optimal_investments tests all possible combinations of stocks to determine the optimal solution.
        :param df: Dataframe that has already been sorted goes here
        :return: total cost, total earnings, and data on the chosen stocks
        """
        price = df['price'].to_list()
        amount_earned = df['amount_earned'].to_list()
        index = len(amount_earned)
        prices = []
        amounts_earned = []
        rmb = self.budget * 100  # rounded multiplied budget

        combination_matrix = [[0 for x in range(rmb + 1)] for x in range(index + 1)]

        for i in range(index + 1):
            for dollar_in_budget in range(rmb + 1):
                if i == 0 or dollar_in_budget == 0:
                    combination_matrix[i][dollar_in_budget] = 0
                elif int(price[i - 1] * 100) <= dollar_in_budget:
                    # checks all possible maximums regardless of whether or not they already exist
                    combination_matrix[i][dollar_in_budget] \
                        = max(amount_earned[i - 1]
                              + combination_matrix[i - 1][dollar_in_budget - int(price[i - 1] * 100)],
                              combination_matrix[i - 1][dollar_in_budget])
                else:
                    combination_matrix[i][dollar_in_budget] = combination_matrix[i - 1][
                        dollar_in_budget]

        # Reconstruction of list of stocks chosen based on the amount_earned and the price constraints
        final_result = combination_matrix[index][rmb]
        reconstruction_budget = rmb
        for i in range(index, 0, -1):
            if final_result <= 0:
                break
            if final_result == combination_matrix[i - 1][reconstruction_budget]:
                continue
            else:
                prices.append(price[i - 1])
                amounts_earned.append(amount_earned[i - 1])
                final_result = final_result - amount_earned[i - 1]
                reconstruction_budget = reconstruction_budget - int(price[i - 1] * 100)
        final_items = []
        associated_prices = []
        for i in range(len(prices)):
            associated_prices.append([prices[i], amounts_earned[i]])
        for item in self.make_items():
            if [item['price'], item['amount_earned']] in associated_prices:
                final_items.append(item)
        return sum(prices), sum(amounts_earned), final_items


if __name__ == "__main__":
    print('For which dataset would you like a Bruteforce investment solution?', '\n', listdir('datasets'))
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
                data_to_be_analyzed = BruteForce(('datasets/' + choice), int(budget_choice))
                print("Format: total_spent, total_earned, stocks_to_buy", '\n',
                      data_to_be_analyzed.determine_optimal_investments(data_to_be_analyzed.sort_and_add_earnings()))
                break
    if custom_budget_choice != 'y':
        data_to_be_analyzed = BruteForce(('datasets/' + choice))
        print("Format: total_spent, total_earned, stocks_to_buy", '\n',
              data_to_be_analyzed.determine_optimal_investments(data_to_be_analyzed.sort_and_add_earnings()))
