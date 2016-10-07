from bs4 import BeautifulSoup
import re

name = []
players = []
play_time = []
age = []
published = []
bgg_link = []

def scrape(filename):
    soup = BeautifulSoup(open(filename), "html.parser")
    title = soup.find("div", {"class": "main-title"})
    name.append(title.text)

    metabar = soup.findAll("div", {"class" : "meta-bar"})
    stats = metabar[0].findAll("strong")
    stats = [x.text for x in stats]
    players.append(stats[0])
    play_time.append(stats[1])
    age.append(stats[2])
    published.append(stats[3])

    for elem in soup(text=re.compile('Game info on BoardGameGeek.com')):
        bgg_link = elem.parent['href']
        break

    store_names = []
    price = []
    status = [] # in stock?
    country = []
    links = []
    free_shipping = []

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
    for table in price_tables:
        table = table.div # avoid the stupid duplicate (class visible-xs shadowed-listing)
        for elem in table.findAll(['a']):
            if elem.text == "Visit Store":
                continue
            store_names.append(elem.text)
            price_elem = elem.parent.parent.next_sibling
            price.append(price_elem.text)
            free_shipping_elem = price_elem.next_sibling
            if free_shipping_elem.span:
                free_shipping.append(free_shipping_elem.span['data-original-title'])
            in_stock_elem = free_shipping_elem.next_sibling
            status.append(in_stock_elem.span.text)
            links.append(elem['href'])

    print(store_names)
    print(price)
    print(free_shipping)
    print(links)
    print(status)



if __name__ == "__main__":
    scrape("codename.html")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    # scrape("sushigoparty.html")
