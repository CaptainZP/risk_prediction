import pandas as pd


df = pd.read_csv("..\\data\\8breakfaith_add_new.csv")

# part1------------------------------------------------------
bins_list1 = list(range(-1, 38, 3)) + [180]
bins_list1_len = len(bins_list1) - 1
df['BF_COUNT_STEP3'] = pd.cut(df['BF_COUNT'], bins=bins_list1, labels=list(range(1, bins_list1_len + 1)), precision=1)

bins_list2 = list(range(-1, 40, 5)) + [180]
bins_list2_len = len(bins_list2) - 1
df['BF_COUNT_STEP5'] = pd.cut(df['BF_COUNT'], bins=bins_list2, labels=list(range(1, bins_list2_len + 1)), precision=1)
print(df)

bins_list3 = [-1, 5, 12, 16, 20, 180]
bins_list3_len = len(bins_list3) - 1
df['BF_COUNT_STEPX1'] = pd.cut(df['BF_COUNT'], bins=bins_list3, labels=list(range(1, bins_list3_len + 1)), precision=1)

bins_list4 = [-1, 12, 20, 180]
bins_list4_len = len(bins_list4) - 1
df['BF_COUNT_STEPX2'] = pd.cut(df['BF_COUNT'], bins=bins_list4, labels=list(range(1, bins_list4_len + 1)), precision=1)

df['BF_COUNT_BIGGER_12'] = df['BF_COUNT'].apply(lambda x: 1 if x > 12 else 0)

df['BF_COUNT_BIGGER_20'] = df['BF_COUNT'].apply(lambda x: 1 if x > 20 else 0)

# get_dummies,4个
df['BF_COUNT_STEP3COPY'] = df['BF_COUNT_STEP3']
df_BF_COUNT_STEP3 = pd.get_dummies(df['BF_COUNT_STEP3COPY'], prefix='BF_COUNT_STEP3')
df_EID_BF_COUNT_STEP3 = pd.concat([df['EID'], df_BF_COUNT_STEP3], axis=1)

df['BF_COUNT_STEP5COPY'] = df['BF_COUNT_STEP5']
df_BF_COUNT_STEP5 = pd.get_dummies(df['BF_COUNT_STEP5COPY'], prefix='BF_COUNT_STEP5')
df_EID_BF_COUNT_STEP5 = pd.concat([df['EID'], df_BF_COUNT_STEP5], axis=1)

df['BF_COUNT_STEPX1COPY'] = df['BF_COUNT_STEPX1']
df_BF_COUNT_STEPX1 = pd.get_dummies(df['BF_COUNT_STEPX1COPY'], prefix='BF_COUNT_STEPX1')
df_EID_BF_COUNT_STEPX1 = pd.concat([df['EID'], df_BF_COUNT_STEPX1], axis=1)

df['BF_COUNT_STEPX2COPY'] = df['BF_COUNT_STEPX2']
df_BF_COUNT_STEPX2 = pd.get_dummies(df['BF_COUNT_STEPX2COPY'], prefix='BF_COUNT_STEPX2')
df_EID_BF_COUNT_STEPX2 = pd.concat([df['EID'], df_BF_COUNT_STEPX2], axis=1)

# part2-----------------------------------------------------
bins_list5 = [-1, 1, 4]
bins_list5_len = len(bins_list5) - 1
df['BF_END_STEP2'] = pd.cut(df['BF_END'], bins=bins_list5, labels=list(range(1, bins_list5_len + 1)), precision=1)

df['BF_END_BIGGER_1'] = df['BF_END'].apply(lambda x: 1 if x > 1 else 0)

# get_dummies,1个
df['BF_END_STEP2COPY'] = df['BF_END_STEP2']
df_BF_END_STEP2 = pd.get_dummies(df['BF_END_STEP2COPY'], prefix='BF_END_STEP2')
df_EID_BF_END_STEP2 = pd.concat([df['EID'], df_BF_END_STEP2], axis=1)

# part3-----------------------------------------------------
bins_list6 = list(range(-1, 38, 3)) + [180]
bins_list6_len = len(bins_list6) - 1
df['BF_IN_STEP3'] = pd.cut(df['BF_IN'], bins=bins_list6, labels=list(range(1, bins_list6_len + 1)), precision=1)

bins_list7 = list(range(-1, 40, 5)) + [180]  # 需要改7处
bins_list7_len = len(bins_list7) - 1
df['BF_IN_STEP5'] = pd.cut(df['BF_IN'], bins=bins_list7, labels=list(range(1, bins_list7_len + 1)), precision=1)

df['BF_IN_BIGGER_20'] = df['BF_IN'].apply(lambda x: 1 if x > 20 else 0)

# get_dummies,2个
df['BF_IN_STEP3COPY'] = df['BF_IN_STEP3']
df_BF_IN_STEP3 = pd.get_dummies(df['BF_IN_STEP3COPY'], prefix='BF_IN_STEP3')
df_EID_BF_IN_STEP3 = pd.concat([df['EID'], df_BF_IN_STEP3], axis=1)

df['BF_IN_STEP5COPY'] = df['BF_IN_STEP5']
df_BF_IN_STEP5 = pd.get_dummies(df['BF_IN_STEP5COPY'], prefix='BF_IN_STEP5')
df_EID_BF_IN_STEP5 = pd.concat([df['EID'], df_BF_IN_STEP5], axis=1)

# part4---------------------------------------------------------
# df_ex = pd.read_csv("..\\data\\8breakfaith.csv")



# merge
df = pd.merge(df, df_EID_BF_COUNT_STEP3, how='left', on='EID')
df = pd.merge(df, df_EID_BF_COUNT_STEP5, how='left', on='EID')
df = pd.merge(df, df_EID_BF_COUNT_STEPX1, how='left', on='EID')
df = pd.merge(df, df_EID_BF_COUNT_STEPX2, how='left', on='EID')
df = pd.merge(df, df_EID_BF_COUNT_STEPX2, how='left', on='EID')
df = pd.merge(df, df_EID_BF_END_STEP2, how='left', on='EID')
df = pd.merge(df, df_EID_BF_IN_STEP3, how='left', on='EID')
df = pd.merge(df, df_EID_BF_IN_STEP5, how='left', on='EID')
df.to_csv('..\\data\\8breakfaith_add_new2.csv', index=False)
