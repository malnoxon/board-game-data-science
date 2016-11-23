import numpy as np
import pandas as pd

df = pd.read_csv("candidate_set_C1_v2.csv")
df2 = df.iloc[np.random.choice(len(df), 400, replace=False)]
df2.to_csv('boardgame_sample_400_v3.csv')
