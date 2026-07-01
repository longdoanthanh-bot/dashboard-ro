import pandas as pd
import json

trip_file = r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Trip\DS-chi-tiet-chuyen-xe_26062026-1017.xlsx"
xnt_file = r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Tồn kho Rổ\XNT_26062026.xlsx"

try:
    df1 = pd.read_excel(trip_file)
    print("TRIP EXCEL COLUMNS:", df1.columns.tolist())
    print("TRIP SAMPLE:")
    print(df1.head(2).to_dict(orient='records'))
except Exception as e:
    print(f"Error reading {trip_file}: {e}")

try:
    df2 = pd.read_excel(xnt_file)
    print("XNT EXCEL COLUMNS:", df2.columns.tolist())
    print("XNT SAMPLE:")
    print(df2.head(2).to_dict(orient='records'))
except Exception as e:
    print(f"Error reading {xnt_file}: {e}")
