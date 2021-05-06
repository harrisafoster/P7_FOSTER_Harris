import pandas as pd
import numpy as np

df = pd.read_csv('sheet1.csv')

sorted_df = df.sort_values(by=['2_year_earnings'], ascending=False)

sorted_df['amount_earned'] = sorted_df['cost'] * sorted_df['2_year_earnings']

budget = 500
spent = 0
stocks_to_buy = []
for value in sorted_df['cost']:
    if spent < 500 and (spent + value) <= 500:
        spent += value
        stocks_to_buy.append(value)

print(spent)
print(stocks_to_buy)
print(sorted_df)