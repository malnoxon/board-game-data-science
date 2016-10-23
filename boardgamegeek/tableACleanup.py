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
# We assume that 0.0/5 scores are due to lack of data/missing values, since webpage renders "--" as value
df['complexity_weight'] = df['complexity_weight'].apply((lambda x: float(re.findall('\d+\.\d*', x)[0]) or np.NaN))

#Rating cleanup
# We assume that rating of 0.0 are caused by missing values, since webpage renders "--" as value
df['rating'] = df['rating'].apply((lambda x: x or np.NaN))

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

print 'Textual category reporting'
text_col = ['id', 'name', 'gameplay_time']
for c in text_col:
    print 'Attribute: ' + c
    lengths = map((lambda x: 0 if pd.isnull(x) else len(x)), df[c])
    print 'Min length: ' + str(min(lengths))
    print 'Max length: ' + str(max(lengths))
    print 'Average length: {0:.4f}'.format(np.mean(lengths))
