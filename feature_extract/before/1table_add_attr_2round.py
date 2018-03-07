import pandas as pd

df = pd.read_csv("..\\data\\1entbase_add_new.csv")

# part1------------------------------------------------------
bins_list1 = list(range(1950, 2016, 1))
bins_list1_len = len(bins_list1) - 1
df['RGYEAR_STEP1'] = pd.cut(df['RGYEAR'], bins=bins_list1, labels=list(range(1, bins_list1_len + 1)), precision=1)

bins_list2 = list(range(1950, 2018, 3))
bins_list2_len = len(bins_list2) - 1
df['RGYEAR_STEP3'] = pd.cut(df['RGYEAR'], bins=bins_list2, labels=list(range(1, bins_list2_len + 1)), precision=1)

bins_list3 = list(range(1950, 2020, 5))
bins_list3_len = len(bins_list3) - 1
df['RGYEAR_STEP5'] = pd.cut(df['RGYEAR'], bins=bins_list3, labels=list(range(1, bins_list3_len + 1)), precision=1)

# get_dummies,3个
df_RGYEAR_STEP1 = pd.get_dummies(df['RGYEAR_STEP1'], prefix='RGYEAR_STEP1')
df_EID_RGYEAR_STEP1 = pd.concat([df['EID'], df_RGYEAR_STEP1], axis=1)

df_RGYEAR_STEP3 = pd.get_dummies(df['RGYEAR_STEP3'], prefix='RGYEAR_STEP3')
df_EID_RGYEAR_STEP3 = pd.concat([df['EID'], df_RGYEAR_STEP3], axis=1)

df_RGYEAR_STEP5 = pd.get_dummies(df['RGYEAR_STEP5'], prefix='RGYEAR_STEP5')
df_EID_RGYEAR_STEP5 = pd.concat([df['EID'], df_RGYEAR_STEP5], axis=1)

# part2-------------------------------------------------------
bins_list4 = list(range(0, 96, 3))
bins_list4_len = len(bins_list4) - 1
df['HY_STEP3'] = pd.cut(df['HY_all'], bins=bins_list4, labels=list(range(1, bins_list4_len + 1)), precision=1)

bins_list5 = list(range(0, 98, 5))
bins_list5_len = len(bins_list5) - 1
df['HY_STEP5'] = pd.cut(df['HY_all'], bins=bins_list5, labels=list(range(1, bins_list5_len + 1)), precision=1)

# get_dummies,2个
df_HY_STEP3 = pd.get_dummies(df['HY_STEP3'], prefix='HY_STEP3')
df_EID_HY_STEP3 = pd.concat([df['EID'], df_HY_STEP3], axis=1)

df_HY_STEP5 = pd.get_dummies(df['HY_STEP5'], prefix='HY_STEP5')
df_EID_HY_STEP5 = pd.concat([df['EID'], df_HY_STEP5], axis=1)

# part3 merge------------------------------------------------------------
df = pd.merge(df, df_EID_RGYEAR_STEP1, how='left', on='EID')
df = pd.merge(df, df_EID_RGYEAR_STEP3, how='left', on='EID')
df = pd.merge(df, df_EID_RGYEAR_STEP5, how='left', on='EID')
df = pd.merge(df, df_EID_HY_STEP3, how='left', on='EID')
df = pd.merge(df, df_EID_HY_STEP5, how='left', on='EID')

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
df['NUM4_1'] = df['MPNUM'] + df['INUM'] + df['FINZB'] + df['FSTINUM']
df['NUM4_2'] = df['MPNUM'] + df['INUM'] + df['FINZB'] + df['TZINUM']
df['NUM4_3'] = df['MPNUM'] + df['INUM'] + df['FSTINUM'] + df['TZINUM']
df['NUM4_4'] = df['MPNUM'] + df['FINZB'] + df['FINZB'] + df['TZINUM']
df['NUM4_5'] = df['INUM'] + df['FINZB'] + df['FINZB'] + df['TZINUM']
df['NUM5'] = df['MPNUM'] + df['INUM'] + df['FINZB'] + df['FSTINUM'] + df['TZINUM']
df['5AVG_NUM'] = df['NUM5']/5
df['4AVG_NUM'] = df['NUM4_3']/5

# 是否有缺失,有几个缺失
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

# 注册资本是否有异常, 归一化
df.to_csv('..\\data\\1entbase_add_new2.csv', index=False)
