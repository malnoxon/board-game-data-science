from bs4 import BeautifulSoup
import re
import csv
import tempfile
import os
import sys

def to_csv(csv_writer, name, players, play_time, age, published, bgg_link, store_names, price, free_shipping, links, status, international):
    with tempfile.SpooledTemporaryFile(max_size=10000, mode='w+') as tmp_file:
        tmp_writer = csv.writer(tmp_file)
        tmp_writer.writerow(store_names)
        tmp_writer.writerow(price)
        tmp_writer.writerow(free_shipping)
        tmp_writer.writerow(links)
        tmp_writer.writerow(status)
        tmp_writer.writerow(international)
        tmp_file.seek(0)
        store_names_joined = tmp_file.readline().strip("\n")
        price_joined = tmp_file.readline().strip("\n")
        free_shipping_joined = tmp_file.readline().strip("\n")
        links_joined = tmp_file.readline().strip("\n")
        status_joined = tmp_file.readline().strip("\n")
        international_joined = tmp_file.readline().strip("\n")

        for i in range(len(store_names)):
            print(store_names[i])

        csv_writer.writerow([name, players, play_time, age, published, bgg_link, store_names_joined, price_joined, free_shipping_joined, links_joined, status_joined, international_joined])


def scrape(filename, csv_writer):
    try:
        soup = BeautifulSoup(open(filename), "html.parser")
        title = soup.find("div", {"class": "main-title"})
        name = ""
        players = ""
        play_time = ""
        age = ""
        published = ""
        bgg_link = ""
        players = ""
        if title:
            name = title.text
        else:
            title = soup.find("div", {"class": "empty-title"})
            # import pdb; pdb.set_trace();
            name = title.h2.span.next_sibling

        metabar = soup.findAll("div", {"class" : "meta-bar"})
        if metabar:
            stats = metabar[0].findAll("strong")
            # stats = [x.text for x in stats]
            for i, e in enumerate(stats):
                if e.next_sibling.text == "# of Players":
                    players = e.text
                if e.next_sibling.text == "Play Time":
                    play_time = e.text
                if e.next_sibling.text == "Age":
                    age = e.text
                if e.next_sibling.text == "Published":
                    published = e.text
            # players = stats[0]
            # play_time = stats[1]
            # age = stats[2]
            # published = stats[3]

        for elem in soup(text=re.compile('Game info on BoardGameGeek.com')):
            bgg_link = elem.parent['href']
            break

        store_names = []
        price = []
        status = [] # in stock?
        country = []
        links = []
        free_shipping = []
        international = []

        # <div id="price-tables"> is US Stores
            # <div data-prices="media-sponsors">
            # <div data-prices="media-usd">
        # <div class="ebay-results"> is ebay
        # <div class="visible-xs shadowed-listing">
            # <div data-prices="media-cnd">
            # <div ddata-prices="media-gbd">
            # <div ddata-prices="media-aus">
            # ...
        # price_table = soup.findAll("div", {"id" : "price-tables"})
        price_tables = soup.findAll("div", {"id" : "price-tables"})
        ebay_table = soup.findAll("div", {"class": "ebay-results"})
        international_table = ebay_table[0].next_sibling.next_sibling
        # print(international_table)
        print("US TABLE")
        # print("**********************************")
        # print("**********************************")
        for table in price_tables:
            # import pdb; pdb.set_trace();
            table = table.div # avoid the stupid duplicate (class visible-xs shadowed-listing)
            for elem in table.findAll(['a']):
                if elem.text == "Visit Store":
                    continue
                print("A")
                store_names.append(elem.text)
                price_elem = elem.parent.next_sibling
                if not price_elem:
                    price_elem = elem.parent.parent.next_sibling
                price.append(price_elem.text)
                print("B")
                free_shipping_elem = price_elem.next_sibling
                if free_shipping_elem.span:
                    free_shipping.append(free_shipping_elem.span['data-original-title'])
                else:
                    free_shipping.append("")
                in_stock_elem = free_shipping_elem.next_sibling
                print("C")
                status.append(in_stock_elem.span.text)
                links.append(elem['href'])
                international.append("False")

        # International table
        # import pdb; pdb.set_trace();
        print("INTERNATIONAL TABLE")
        # import pdb; pdb.set_trace();
        if 'class' in international_table.attrs and international_table['class'] == ["hidden-xs"]:
            for table in [international_table]:
                for elem in table.findAll(['a']):
                    if elem.text == "Visit Store":
                        continue
                    store_names.append(elem.text)
                    price_elem = elem.parent.next_sibling
                    if not price_elem:
                        price_elem = elem.parent.parent.next_sibling
                    price.append(price_elem.text)
                    free_shipping_elem = price_elem.next_sibling
                    if free_shipping_elem.span:
                        # free_shipping.append(BeautifulSoup(free_shipping_elem.span['data-original-title'], "html.parser").b.text)
                        free_shipping.append(free_shipping_elem.span['data-original-title'])
                    else:
                        free_shipping.append("")
                    in_stock_elem = free_shipping_elem.next_sibling
                    status.append(in_stock_elem.span.text)
                    links.append(elem['href'])
                    international.append("True")


        print(store_names)
        print(price)
        print(free_shipping)
        print(links)
        print(status)
        print(international)

        to_csv(csv_writer, name, players, play_time, age, published, bgg_link, store_names, price, free_shipping, links, status, international)

    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        print(e)
        # import pdb; pdb.post_mortem();



if __name__ == "__main__":
    with open('test.out', 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        headers = ["name", "number of players", "play time", "reccomended ages", "published", "BGG link", "store names", "store prices", "shipping information", "link to buy", "availability", "international store"]
        csv_writer.writerow(headers)
        for filename in os.listdir("/home/xeno/repos/board-game-data-science/boardgameprices/samples"):
            if filename.endswith(".html"):
                scrape(filename, csv_writer)
        # scrape("BGP_academy.html", csv_writer)
        # scrape("BGP_ad30.html", csv_writer)
        # scrape("codename.html", csv_writer)
        # print("------------------------------------------------------------")
        # print("------------------------------------------------------------")
        # print("------------------------------------------------------------")
        # scrape("sushigoparty.html", csv_writer)
