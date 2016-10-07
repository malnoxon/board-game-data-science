from bs4 import BeautifulSoup
import pandas as pd

soup = BeautifulSoup(open('data/stratego-transformers.html'))

columns = ['name', 'year, ''overall_rank', 'avg_rating' 
           'num_players','time' , 'age', 'complexity_weight']
df = pd.DataFrame(columns=columns)
row = {}

header = soup.find('div', class_='game-header-title-container'))
