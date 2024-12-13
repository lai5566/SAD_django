import pandas as pd
import xlrd

import pyxlsb
# 定義檔案路徑
file_path = "static/課程查詢_1131130204122.xls"

# 讀取 Excel 文件，跳過前 5 行
try:
    df = pd.read_excel(file_path, skiprows=4,engine='xlrd')
    print("資料表讀取成功，顯示前幾行：")
    print(df.head())
except Exception as e:
    print(f"讀取檔案錯誤: {e}")


print(df.dtypes)