import pandas as pd
import numpy as np

df = pd.read_csv("..\\data\\1entbase_add_new.csv")
df['IF_MPNUM_NULL'] = df['MPNUM'].isnull()
df['IF_INUM_NULL'] = df['INUM'].isnull()
df['IF_FINZB_NULL'] = df['FINZB'].isnull()
df['IF_FSTINUM_NULL'] = df['FSTINUM'].isnull()
df['IF_TZINUM_NULL'] = df['TZINUM'].isnull()

df['IF_MPNUM_NULL'] = df['IF_MPNUM_NULL'].apply(lambda x: 1 if x is True else 0)
df['IF_INUM_NULL'] = df['IF_INUM_NULL'].apply(lambda x: 1 if x is True else 0)
df['IF_FINZB_NULL'] = df['IF_FINZB_NULL'].apply(lambda x: 1 if x is True else 0)
df['IF_FSTINUM_NULL'] = df['IF_FSTINUM_NULL'].apply(lambda x: 1 if x is True else 0)
df['IF_TZINUM_NULL'] = df['IF_TZINUM_NULL'].apply(lambda x: 1 if x is True else 0)

df['NUM_NULL_NUM'] = df['IF_MPNUM_NULL'] + df['IF_INUM_NULL'] + df['IF_FINZB_NULL'] + df['IF_FSTINUM_NULL'] + df['IF_TZINUM_NULL']
print(df['NUM_NULL_NUM'])

