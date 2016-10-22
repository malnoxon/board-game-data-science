import csv

# This file converts the tableB that we parsed and then added a unique id to the first row of and then modifies the schema to be the same as tableA

with open('tableB.csv', 'r') as csv_in:
    with open('tableB_combined_schema.csv', 'w') as csv_out:
        csv_writer = csv.writer(csv_out)
        csv_reader = csv.reader(csv_in)
        out_headers = ["id", "name", "year", "rating", "rank", "num_players", "gameplay_time", "age", "complexity_weight", "category", "mechanisms", "type", "BGG_link", "store_names", "store_prices", "links_to_buy", "availability", "international_store"]

        csv_writer.writerow(out_headers)
        for row in csv_reader:
            csv_writer.writerow([row[0], row[1], row[5], "", "", row[2], row[3], row[4], "", "", "", "", row[6], row[7], row[8], row[9], row[10], row[11]])

