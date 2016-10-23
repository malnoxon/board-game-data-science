import re
import numpy as np
import pandas as pd

def gen_min_player(x):
    if pd.isnull(x):
        return x
    try:
        return int(x) 
    except ValueError:
        return int(re.findall('\d+', x)[0])

def gen_max_player(x):
    if pd.isnull(x):
        return x
    try:
        return int(x) 
    except ValueError:
        return int(re.findall('\d+', x)[1])

df = pd.read_csv(open('TableA.csv', 'rb'))

# Munge min/max players
df['min_players'] = df['num_players'].apply(gen_min_player)
df['max_players'] = df['num_players'].apply(gen_max_player)

# Age cleanup
df['age'] = df['age'].apply((lambda x: x if pd.isnull(x) else int(re.findall('\d+', x)[0])))

#complexity_weight cleanup
df['complexity_weight'] = df['complexity_weight'].apply((lambda x: None if not x else float(re.findall('\d+\.\d*', x)[0])))

# Slice schema columns
columns = ['id', 'name', 'year', 'age', 'min_players', 'max_players', 'gameplay_time', 'complexity_weight', 'rating']
df = df[columns]

print 'Head of cleaned up TableA'
print df.head()

print 'Calculating missing values'
total_entries = len(df)
for c in columns:
    print 'Attribute: ' + c
    percent = 100.0*(float(sum(pd.isnull(df[c])))/total_entries)
    print 'Percentage missing: {0:.6f}%'.format(percent)
