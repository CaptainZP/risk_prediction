import pandas as pd

df = pd.read_csv("..\\data\\1entbase.csv")

# part1------------------------------------------------------
bins_list2 = list(range(1926, 2018, 3))
bins_list2_len = len(bins_list2) - 1
df['RGYEAR_STEP3'] = pd.cut(df['RGYEAR'], bins=bins_list2, labels=list(range(1, bins_list2_len + 1)), precision=1)

# get_dummies
df_RGYEAR_STEP3 = pd.get_dummies(df['RGYEAR_STEP3'], prefix='RGYEAR_STEP3')
df_EID_RGYEAR_STEP3 = pd.concat([df['EID'], df_RGYEAR_STEP3], axis=1)

# part2-------------------------------------------------------
bins_list4 = list(range(0, 99, 3))
bins_list4_len = len(bins_list4) - 1
df['HY_STEP3'] = pd.cut(df['HY'], bins=bins_list4, labels=list(range(1, bins_list4_len + 1)), precision=1)

# get_dummies
df_HY_STEP3 = pd.get_dummies(df['HY_STEP3'], prefix='HY_STEP3')
df_EID_HY_STEP3 = pd.concat([df['EID'], df_HY_STEP3], axis=1)

# part3 merge------------------------------------------------------------
df_RGYEAR = pd.get_dummies(df['RGYEAR'], prefix='RGYEAR')
df_EID_RGYEAR = pd.concat([df['EID'], df_RGYEAR], axis=1)
df_HY = pd.get_dummies(df['HY'], prefix='HY')
df_EID_HY = pd.concat([df['EID'], df_HY], axis=1)
df_ETYPE = pd.get_dummies(df['ETYPE'], prefix='ETYPE')
df_EID_ETYPE = pd.concat([df['EID'], df_ETYPE], axis=1)

df = pd.merge(df, df_EID_RGYEAR_STEP3, how='left', on='EID')
df = pd.merge(df, df_EID_HY_STEP3, how='left', on='EID')
df = pd.merge(df, df_EID_RGYEAR, how='left', on='EID')
df = pd.merge(df, df_EID_HY, how='left', on='EID')
df = pd.merge(df, df_EID_ETYPE, how='left', on='EID')

# part4------------------------------------------------------------
df['NUM2_1'] = df['MPNUM'] + df['INUM']
df['NUM2_2'] = df['MPNUM'] + df['FINZB']
df['NUM2_3'] = df['MPNUM'] + df['FSTINUM']
df['NUM2_4'] = df['MPNUM'] + df['TZINUM']
df['NUM2_5'] = df['INUM'] + df['FINZB']
df['NUM2_6'] = df['INUM'] + df['FSTINUM']
df['NUM2_7'] = df['INUM'] + df['TZINUM']
df['NUM2_8'] = df['FINZB'] + df['FSTINUM']
df['NUM2_9'] = df['FINZB'] + df['TZINUM']
df['NUM2_10'] = df['FSTINUM'] + df['TZINUM']
df['NUM2_11'] = df['ENUM'] + df['MPNUM']
df['NUM2_12'] = df['ENUM'] + df['INUM']
df['NUM2_13'] = df['ENUM'] + df['FINZB']
df['NUM2_14'] = df['ENUM'] + df['TZINUM']
df['NUM2_15'] = df['ENUM'] + df['FSTINUM']

df['NUM3_1'] = df['MPNUM'] + df['INUM'] + df['FINZB']
df['NUM3_2'] = df['MPNUM'] + df['INUM'] + df['FSTINUM']
df['NUM3_3'] = df['MPNUM'] + df['INUM'] + df['TZINUM']
df['NUM3_4'] = df['MPNUM'] + df['FINZB'] + df['FSTINUM']
df['NUM3_5'] = df['MPNUM'] + df['FINZB'] + df['TZINUM']
df['NUM3_6'] = df['MPNUM'] + df['FSTINUM'] + df['TZINUM']
df['NUM3_7'] = df['INUM'] + df['FINZB'] + df['FSTINUM']
df['NUM3_8'] = df['INUM'] + df['FINZB'] + df['TZINUM']
df['NUM3_9'] = df['INUM'] + df['FSTINUM'] + df['TZINUM']
df['NUM3_10'] = df['FINZB'] + df['FSTINUM'] + df['TZINUM']
df['NUM3_11'] = df['ENUM'] + df['MPNUM'] + df['INUM']
df['NUM3_12'] = df['ENUM'] + df['MPNUM'] + df['FINZB']
df['NUM3_13'] = df['ENUM'] + df['MPNUM'] + df['TZINUM']
df['NUM3_14'] = df['ENUM'] + df['MPNUM'] + df['FSTINUM']
df['NUM3_15'] = df['ENUM'] + df['FINZB'] + df['TZINUM']
df['NUM3_16'] = df['ENUM'] + df['FINZB'] + df['FSTINUM']
df['NUM3_17'] = df['ENUM'] + df['TZINUM'] + df['FSTINUM']
df['NUM3_18'] = df['ENUM'] + df['INUM'] + df['FINZB']
df['NUM3_19'] = df['ENUM'] + df['INUM'] + df['TZINUM']
df['NUM3_20'] = df['ENUM'] + df['INUM'] + df['FSTINUM']

df['NUM4_1'] = df['MPNUM'] + df['INUM'] + df['FINZB'] + df['FSTINUM']
df['NUM4_2'] = df['MPNUM'] + df['INUM'] + df['FINZB'] + df['TZINUM']
df['NUM4_3'] = df['MPNUM'] + df['INUM'] + df['FSTINUM'] + df['TZINUM']
df['NUM4_4'] = df['MPNUM'] + df['FINZB'] + df['FINZB'] + df['TZINUM']
df['NUM4_5'] = df['INUM'] + df['FINZB'] + df['FINZB'] + df['TZINUM']
df['NUM4_6'] = df['ENUM'] + df['MPNUM'] + df['INUM'] + df['FINZB']
df['NUM4_7'] = df['ENUM'] + df['MPNUM'] + df['INUM'] + df['FSTINUM']
df['NUM4_8'] = df['ENUM'] + df['MPNUM'] + df['INUM'] + df['TZINUM']
df['NUM4_9'] = df['ENUM'] + df['MPNUM'] + df['FINZB'] + df['FSTINUM']
df['NUM4_10'] = df['ENUM'] + df['MPNUM'] + df['FINZB'] + df['TZINUM']
df['NUM4_11'] = df['ENUM'] + df['MPNUM'] + df['FSTINUM'] + df['TZINUM']
df['NUM4_12'] = df['ENUM'] + df['INUM'] + df['FINZB'] + df['FSTINUM']
df['NUM4_13'] = df['ENUM'] + df['INUM'] + df['FINZB'] + df['TZINUM']
df['NUM4_14'] = df['ENUM'] + df['INUM'] + df['FSTINUM'] + df['TZINUM']
df['NUM4_15'] = df['ENUM'] + df['FINZB'] + df['FSTINUM'] + df['TZINUM']

df['NUM5_1'] = df['MPNUM'] + df['INUM'] + df['FINZB'] + df['FSTINUM'] + df['TZINUM']
df['NUM5_2'] = df['ENUM'] + df['MPNUM'] + df['INUM'] + df['FINZB'] + df['TZINUM']
df['NUM5_3'] = df['ENUM'] + df['MPNUM'] + df['INUM'] + df['FSTINUM'] + df['TZINUM']
df['NUM5_4'] = df['ENUM'] + df['MPNUM'] + df['FINZB'] + df['FINZB'] + df['TZINUM']
df['NUM5_5'] = df['ENUM'] + df['INUM'] + df['FINZB'] + df['FINZB'] + df['TZINUM']

df['NUM6'] = df['ENUM'] + df['MPNUM'] + df['INUM'] + df['FINZB'] + df['FSTINUM'] + df['TZINUM']

df['6AVG_NUM'] = df['NUM6']/6
df['5AVG_NUM'] = df['NUM5_3']/5

# 是否有缺失,有几个缺失
df['IF_MPNUM_NULL'] = df['MPNUM'].isnull()
df['IF_INUM_NULL'] = df['INUM'].isnull()
df['IF_FINZB_NULL'] = df['FINZB'].isnull()
df['IF_FSTINUM_NULL'] = df['FSTINUM'].isnull()
df['IF_TZINUM_NULL'] = df['TZINUM'].isnull()
df['IF_ENUM_NULL'] = df['ENUM'].isnull()

df['IF_MPNUM_NULL'] = df['IF_MPNUM_NULL'].apply(lambda x: 1 if x is True else 0)
df['IF_INUM_NULL'] = df['IF_INUM_NULL'].apply(lambda x: 1 if x is True else 0)
df['IF_FINZB_NULL'] = df['IF_FINZB_NULL'].apply(lambda x: 1 if x is True else 0)
df['IF_FSTINUM_NULL'] = df['IF_FSTINUM_NULL'].apply(lambda x: 1 if x is True else 0)
df['IF_TZINUM_NULL'] = df['IF_TZINUM_NULL'].apply(lambda x: 1 if x is True else 0)
df['IF_ENUM_NULL'] = df['IF_ENUM_NULL'].apply(lambda x: 1 if x is True else 0)

df['NUM_NULL_NUM'] = df['IF_MPNUM_NULL'] + df['IF_INUM_NULL'] + df['IF_FINZB_NULL'] + df['IF_FSTINUM_NULL'] + df['IF_TZINUM_NULL'] + df['IF_ENUM_NULL']

# 注册资本是否有异常, 归一化
df.to_csv('..\\data\\1entbase_add.csv', index=False)
