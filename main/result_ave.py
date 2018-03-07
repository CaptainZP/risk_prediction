import pandas as pd


'''
xgb与lgm融合提高0.01
lgm_bb与lgm融合提高0.017
上面两种分别融合后，再融合无提高
'''

result1 = "result_lgm_12_8_1"
result2 = "result_lgm_12_5_3"  # 结果更好一点
ave_result = "result_ave_12_8_2"
method = 2

df_xgb = pd.read_csv("C:\\Users\\captainzp\\Desktop\\result\\{}.csv".format(result1))
df_lgm = pd.read_csv("C:\\Users\\captainzp\\Desktop\\result\\{}.csv".format(result2))

if method == 1:
    # 融合方法1
    ave_EID = df_xgb['EID']
    ave_FORTARGET = df_xgb['FORTARGET'] & df_lgm['FORTARGET']  # 0/1进行与操作
    ave_PROB = df_xgb['PROB']*0.4 + df_lgm['PROB']*0.6
    df = pd.DataFrame({'EID': ave_EID, 'FORTARGET': ave_FORTARGET, 'PROB': ave_PROB})
else:
    # 融合方法2
    ave_EID = df_xgb['EID']
    ave_FORTARGET = df_xgb['FORTARGET']  # temp target
    ave_PROB = df_xgb['PROB']*0.4 + df_lgm['PROB']*0.6
    df = pd.DataFrame({'EID': ave_EID, 'FORTARGET': ave_FORTARGET, 'PROB': ave_PROB})
    df['FORTARGET'] = df['PROB'].apply(lambda x: 1 if x > 0.16 else 0)  # 根据概率取0/1

df.to_csv('C:\\Users\\captainzp\\Desktop\\{}.csv'.format(ave_result), index=False)
