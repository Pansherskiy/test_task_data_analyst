import pandas as pd
from tabulate import tabulate


data = pd.read_csv('task/data.csv')['event']

df = pd.DataFrame(data=data.value_counts().to_dict(), index=['count'])
df.loc['percentage'] = round(df.loc['count'] / df.loc['count'].sum() * 100, 2)
total = df.sum(axis=1)
df['Total'] = total


print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
