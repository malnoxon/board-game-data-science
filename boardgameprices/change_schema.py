import csv
import re
import pandas as pd

# This file converts the tableB that we parsed and then added a unique id to the first row of and then modifies the schema to be the same as tableA


def gen_min_player(x):
    if x == '':
        return x
    try:
        return int(x) 
    except ValueError:
        try:
            return int(re.findall('\d+', x)[0])
        except:
            import pdb; pdb.set_trace();

def gen_max_player(x):
    if x == '':
        return x
    try:
        return int(x) 
    except ValueError:
        return int(re.findall('\d+', x)[1])

def gen_min_gameplay_time(x):
    if x == '':
        return x
    return int(re.findall('\d+', x)[0])

def gen_max_gameplay_time(x):
    if x == '':
        return x
    values = re.findall('\d+', x)
    if len(values) == 2:
        return int(values[1])
    else:
        return int(values[0])


with open('tableB.csv', 'r') as csv_in:
    with open('tableB_combined_schema.csv', 'w') as csv_out:
        csv_writer = csv.writer(csv_out)
        csv_reader = csv.reader(csv_in)
        out_headers = ["id", "name", "year", "rating", "rank", "num_players", "min_num_players", "max_num_players", "gameplay_time", "min_gameplay_time", "max_gameplay_time", "age", "complexity_weight", "category", "mechanisms", "type", "BGG_link", "store_names", "store_prices", "links_to_buy", "availability", "international_store"]

        csv_writer.writerow(out_headers)
        first_row = True
        for row in csv_reader:
            if not first_row:
                min_num_players = gen_min_player(row[2])
                max_num_players = gen_max_player(row[2])
                min_gameplay_time = gen_min_gameplay_time(row[3])
                max_gameplay_time = gen_max_gameplay_time(row[3])
                csv_writer.writerow([row[0], row[1], row[5], "", "", row[2], min_num_players, max_num_players, row[3], min_gameplay_time, max_gameplay_time, row[4], "", "", "", "", row[6], row[7], row[8], row[9], row[10], row[11]])
            first_row = False

