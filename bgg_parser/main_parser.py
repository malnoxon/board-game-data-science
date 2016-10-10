from bs4 import BeautifulSoup
import pandas as pd
import re
from os import listdir
from os.path import isfile, join
import sys

def clean_raw(s):
    return re.sub(u"\u2013", "-", re.sub('\t', '', s)).strip()

def parse_bgg_page(url):
    game_divs = BeautifulSoup(open(url),"html.parser").find_all('div',class_='game')
    if (not game_divs):
        raise Exception('GeekItem does not exist/not a game')
    elif (len(game_divs) < 2):
        raise Exception('Game data not loaded')
    soup = game_divs[1]


    row = {}
    # First is the loading-version, second is the loaded version
    header = soup.find('div', class_='game-header-body')
    row['name'] = clean_raw(header.find('div', class_='game-header-title-info').h1.a.text)
    row['year'] = re.findall("\d+", clean_raw(header.h1.span.text))[0]
    row['rating'] = re.findall("\d+\.\d+", clean_raw(header.find('a', 'rating-overall-callout').text))[0]


    #Gameplay characteristics
    gameplay = header.find('ul', 'gameplay').find_all('li')
    row['num_players'] = gameplay[0].find('div', 'gameplay-item-primary').span.text
    row['gameplay_time'] = clean_raw(gameplay[1].find('div', 'gameplay-item-primary').span.text)
    row['age'] = clean_raw(gameplay[2].find('div', 'gameplay-item-primary').span.text)
    row['complexity_weight'] = clean_raw(
            gameplay[3].find('div', 'gameplay-item-primary').find_all('span')[1].text
        ).replace(' ', '')


    # Get Classification data
    class_table = soup.find('classifications-module')
    features = class_table.find_all('li', class_='feature')

    # Type
    row['type'] = ';'.join(map(
        (lambda x: clean_raw(x.text)),
        features[0].find("div", "feature-description").find_all('span')
    ))

    # Category
    row['category'] = ';'.join(map(
        (lambda x: clean_raw(x.text)),
        features[1].find("div", "feature-description").find_all('span', 'text-block')
    ))

    # Mechanisms
    row['mechanisms'] = ';'.join(map(
        (lambda x: clean_raw(x.text)),
        features[2].find("div", "feature-description").find_all('span', 'text-block')
    ))

    # Family
    row['type'] = ';'.join(map(
        (lambda x: clean_raw(x.text)),
        features[3].find("div", "feature-description").find_all('span', 'text-block')
    ))

    return row



def parse_bgg_folder(mypath):
    columns = ['name', 'year', 'rating',
               'num_players','gameplay_time' , 'age', 'complexity_weight',
               'category', 'mechanisms', 'type']
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    df = pd.DataFrame(columns=columns)
    for page in onlyfiles:
        try:
            df = df.append(pd.Series(parse_bgg_page(mypath+page)), ignore_index=True)
        except Exception as e:
            print page +': '+ str(e)
            continue

    df.to_csv(mypath+'bgg_data.csv', encoding='utf-8')
    

parse_bgg_folder(sys.argv[1])
