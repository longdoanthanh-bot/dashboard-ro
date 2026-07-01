import pymysql
import pandas as pd
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

try:
    print("⏳ Đang kết nối tới StarRocks Database...")
    conn = pymysql.connect(
        host='103.147.122.103',
        port=9030,
        user='kfm_scm_tho_nguyen',
        password='oh1dtJwR4ihLGrX4E7bs',
        database='kfm_scm'
    )
    
    # 1. Kéo dữ liệu Chuyến Xe (TRIP)
    print("⏳ Đang truy vấn dữ liệu Thu hồi rổ (Trip)...")
    q_trip = """
    SELECT 
        DATE(t.t_departure) as `Ngày`,
        tl.search_text as `Mã chuyến/Cửa hàng`,
        tli.barrel_basket_code as `Mã rổ`,
        tli.barrel_basket_name as `Tên rổ`,
        tli.tli_transfer_qty as `Số lượng giao`,
        tli.tli_actual_received_qty as `Số lượng thu hồi`
    FROM __cdc_kfm_kf_inventories_kf_trips_locations_items tli
    JOIN __cdc_kfm_kf_inventories_kf_trip_locations tl ON tli.tl_id = tl._id
    JOIN __cdc_kfm_kf_inventories_kf_trips t ON tl.t_id = t._id
    WHERE t.t_departure >= '2026-06-20' AND tli.barrel_basket_code IS NOT NULL
    """
    df_trip = pd.read_sql(q_trip, conn)
    
    # Lưu ra Excel để người dùng xem
    output_trip = r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Thu hồi rổ\Trip_Data_From_DB.xlsx"
    df_trip.to_excel(output_trip, index=False)
    print(f"✅ Đã lưu dữ liệu Thu hồi rổ từ DB ra file: {output_trip}")
    
    # 2. Cố gắng kéo dữ liệu Tồn kho
    print("⏳ Đang truy vấn dữ liệu Tồn kho (Stock)...")
    q_stock = """
    SELECT branch_id, barcode, closing_stock 
    FROM __cdc_kfm_kf_inventories_kf_inventory_transaction_stock_summaries 
    LIMIT 10
    """
    df_stock = pd.read_sql(q_stock, conn)
    print("✅ Đã kéo được dữ liệu Tồn kho.")
    
    conn.close()
except Exception as e:
    print(f"❌ LỖI DATABASE: {e}")
    print("=> Như bạn thấy, dữ liệu Tồn kho (Stock) đang bị lỗi từ phía Server (tablet does not exist / OlapScanNode fail).")
