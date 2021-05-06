import pandas as pd
import numpy as np

df = pd.read_csv('sheet1.csv')

sorted_df = df.sort_values(by=['2_year_earnings'], ascending=False)

sorted_df['amount_earned'] = sorted_df['cost'] * sorted_df['2_year_earnings']

budget = 500
spent = 0
earned = 0
stocks_to_buy = []
for index, row in sorted_df.iterrows():
    if spent < 500 and (spent + row['cost']) <= 500:
        spent += row['cost']
        earned += row['amount_earned']
        stocks_to_buy.append(row['name'])

print(spent)
print(earned)
print(stocks_to_buy)
print(sorted_df)