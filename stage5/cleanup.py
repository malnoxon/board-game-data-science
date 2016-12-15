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

def gen_min_gameplay_time(x):
    if pd.isnull(x):
        return x
    return int(re.findall('\d+', x)[0])

def gen_max_gameplay_time(x):
    if pd.isnull(x):
        return x
    values = re.findall('\d+', x)
    if len(values) == 2:
        return int(values[1])
    else:
        return int(values[0])
def gen_min_price(x):
    if pd.isnull(x):
        return x
    try:
        return int(x) 
    except ValueError:
        prices = []
        curr_str = ''
        for p in x:
            if p == ',':
                if curr_str != '':
                    prices.append(float(curr_str)) 
                curr_str = ''
            elif p in '0123456789.':
                curr_str += p
        if curr_str != '':
            prices.append(float(curr_str)) 
        
        return min(prices)

def gen_max_price(x):
    if pd.isnull(x):
        return x
    try:
        return int(x) 
    except ValueError:
        prices = []
        curr_str = ''
        for p in x:
            if p == ',':
                if curr_str != '':
                    prices.append(float(curr_str)) 
                curr_str = ''
            elif p in '0123456789.':
                curr_str += p
        if curr_str != '':
            prices.append(float(curr_str)) 
        
        return max(prices)

def gen_mean_price(x):
    if pd.isnull(x):
        return x
    try:
        return int(x) 
    except ValueError:
        prices = []
        curr_str = ''
        for p in x:
            if p == ',':
                if curr_str != '':
                    prices.append(float(curr_str)) 
                curr_str = ''
            elif p in '0123456789.':
                curr_str += p
        if curr_str != '':
            prices.append(float(curr_str)) 
        
        return sum(prices)/len(prices)

df = pd.read_csv(open('joined_table.csv', 'rb'))

df['min_price'] = df['store_prices'].apply(gen_min_price)
df['max_price'] = df['store_prices'].apply(gen_max_price)
df['mean_price'] = df['store_prices'].apply(gen_mean_price)

# # Munge min/max players
# df['min_players'] = df['num_players'].apply(gen_min_player)
# df['max_players'] = df['num_players'].apply(gen_max_player)
#
# # Age cleanup
# df['min_age'] = df['age'].apply((lambda x: x if pd.isnull(x) else int(re.findall('\d+', x)[0])))
#
# #complexity_weight cleanup
# # We assume that 0.0/5 scores are due to lack of data/missing values, since webpage renders "--" as value
# df['complexity_weight'] = df['complexity_weight'].apply((lambda x: float(re.findall('\d+\.\d*', x)[0]) or np.NaN))
#
# #Rating cleanup
# # We assume that rating of 0.0 are caused by missing values, since webpage renders "--" as value
# df['rating'] = df['rating'].apply((lambda x: x or np.NaN))
#
# #gameplay_time cleanup
# df['min_gameplay_time'] = df['gameplay_time'].apply(gen_min_gameplay_time)
# df['max_gameplay_time'] = df['gameplay_time'].apply(gen_max_gameplay_time)
#
# # Slice schema columns
# columns = ['id', 'name', 'year', 'rating', 'rank', 'min_players', 'max_players', 'min_gameplay_time', 'max_gameplay_time', 'min_age', 'complexity_weight', 'category', 'mechanisms','type']
# df = df[columns]
# df['BGG_link'] = np.nan
# df['store_names'] = np.nan
# df['store_prices'] = np.nan
# df['links_to_buy'] = np.nan
# df['availability'] = np.nan
# df['international_store'] = np.nan
#
df.to_csv('new_joined_table.csv')
#
# print 'Head of cleaned up TableA'
# print df.head()
#
# print 'Calculating missing values'
# total_entries = len(df)
# for c in columns:
#     print 'Attribute: ' + c
#     percent = 100.0*(float(sum(pd.isnull(df[c])))/total_entries)
#     print '> Percentage missing: {0:.6f}%'.format(percent)
#     print '> Fraction missing: '+str(sum(pd.isnull(df[c]))) + '/'+str(total_entries)
#
# print 'Textual category reporting'
# text_col = ['name', 'type', 'category']
# for c in text_col:
#     print 'Attribute: ' + c
#     lengths = map(len, filter((lambda x: not pd.isnull(x)), df[c]))
#     print 'Min length: ' + str(min(lengths))
#     print 'Max length: ' + str(max(lengths))
#     print 'Average length: {0:.4f}'.format(np.mean(lengths))
#     
#
# print 'Histogram analysis'
#
# print 'Attribute: name'
# lengths = map((lambda x: 0 if pd.isnull(x) else len(x)), df[c])
#     
