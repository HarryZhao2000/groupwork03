import pandas as pd
df = pd.read_csv("data_v4.4.csv", comment="#", header=0, sep=" ", index_col="lv")
pd.concat([df, df['hour'] - df['hour'].shift(1).fillna(0)], axis=1)
df['diff'].hist()