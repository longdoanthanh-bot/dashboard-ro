import pymysql
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    conn = pymysql.connect(
        host='103.147.122.103',
        port=9030,
        user='kfm_scm_tho_nguyen',
        password='oh1dtJwR4ihLGrX4E7bs',
        database='kfm_scm'
    )
    
    q_stock = "SELECT * FROM krc_dashboard_erp_stock_summary LIMIT 20;"
    df_stock = pd.read_sql(q_stock, conn)
    print("ERP STOCK SUMMARY DATA:")
    print(df_stock.to_string())
    
    conn.close()
except Exception as e:
    print(e)
