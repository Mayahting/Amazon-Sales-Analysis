import pandas as pd
import sqlite3
df = pd.read_csv('C:/Users/mayath1ng/AppData/Local/YunDong/Amazon Sale Report.csv',encoding='utf-8',on_bad_lines='skip') #前者防止乱码，后者

print("表格形状（行，列: ",df.shape)
print("每列缺失数据量：",df.isnull().sum())

print(df[df['Amount'].isnull()][['Order ID','Qty','Amount','ship-state']].head())
print(df[df['Qty'].isnull()][['Order ID','Qty','Amount','ship-state']].head())
print(len(df[df['Amount']<=0]))

print("\n--- 开始清洗 ---")
print("清洗前的数据行数：",len(df))
df_clean = df.dropna(subset=['Amount','Qty'])
df_clean = df_clean[df_clean['Amount']>0]

df_clean = df_clean.rename(columns={'Order ID':'order id','ship-state':'ship_state','ship-city':'ship_city'})

conn = sqlite3.connect('company_data.db')
cols = ['order id','Date','Status','Category','Qty','Amount','ship_state']
df_final = df_clean[cols]
print(f"保留了: {len(df_final)}行有效数据")
df_final.to_sql('amazon_sales',conn,if_exists='replace',index=False)

sql_query= """
SELECT
ship_state ,
SUM(Amount) AS total_sales,
SUM(Qty) AS total_qty
FROM amazon_sales
GROUP BY ship_state
ORDER BY total_sales DESC
LIMIT 5;
"""
result = pd.read_sql_query(sql_query,conn)
print(result)
conn.close()

