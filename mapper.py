import pymysql
import pandas as pd
import json

xnt_file = r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Tồn kho Rổ\XNT_26062026.xlsx"
df_excel = pd.read_excel(xnt_file)

# Build a signature for each store from Excel
# For a store, its signature is a tuple of quantities of specific items.
# Let's say: [Q1, Q2, Q3, ...] for the items in XNT_MAPPING.
XNT_MAPPING_NAMES = [
    "Rổ nhựa đen/xanh lá kho rau",
    "Seedlog - Thùng tote xanh lá, xanh dương không đục lỗ",
    "Rổ đen xếp chồng quai đỏ",
    "Rổ cam xếp chồng quai đỏ (sóng nhựa hở BPGST-25V KT: 600x400x250)",
    "Rổ ABA đông mát",
    "Tote ABA đông mát",
    "Tote đỏ bánh tươi"
]

barcode_map = {
    "Rổ nhựa đen/xanh lá kho rau": "CC00357",
    "Seedlog - Thùng tote xanh lá, xanh dương không đục lỗ": "CC00359",
    "Rổ đen xếp chồng quai đỏ": "CC00360",
    "Rổ cam xếp chồng quai đỏ (sóng nhựa hở BPGST-25V KT: 600x400x250)": "CC00362",
    "Rổ ABA đông mát": "CC00376",
    "Tote ABA đông mát": "CC00377",
    "Tote đỏ bánh tươi": "CC00381"
}

excel_store_sig = {}
for chi_nhanh, group in df_excel.groupby('Chi nhánh'):
    sig = {}
    for name in XNT_MAPPING_NAMES:
        row = group[group['Tên hàng'] == name]
        if not row.empty:
            val = row['Tồn cuối kỳ'].values[0]
            if pd.isna(val): val = 0
            sig[barcode_map[name]] = int(val)
        else:
            sig[barcode_map[name]] = 0
    excel_store_sig[chi_nhanh] = sig

# Now read DB
try:
    conn = pymysql.connect(
        host='103.147.122.103',
        port=9030,
        user='kfm_scm_tho_nguyen',
        password='oh1dtJwR4ihLGrX4E7bs',
        database='kfm_scm'
    )
    
    # We want latest closing_stock for each branch_id, barcode
    barcodes = tuple(barcode_map.values())
    q = f"""
    SELECT branch_id, barcode, closing_stock
    FROM __cdc_kfm_kf_inventories_kf_inventory_transaction_stock_summaries
    WHERE barcode IN {barcodes} AND closing_stock IS NOT NULL
    """
    df_db = pd.read_sql(q, conn)
    conn.close()
    
    # Actually, the DB has multiple rows for the same branch_id + barcode due to CDC or history? 
    # The table might be just latest summary. If there are duplicates, we group by branch_id, barcode and sum or take max/latest?
    # Let's check duplicates
    df_db = df_db.sort_values('closing_stock', ascending=False).drop_duplicates(['branch_id', 'barcode'])
    
    db_store_sig = {}
    for branch_id, group in df_db.groupby('branch_id'):
        sig = {}
        for b in barcodes:
            row = group[group['barcode'] == b]
            if not row.empty:
                sig[b] = int(row['closing_stock'].values[0])
            else:
                sig[b] = 0
        db_store_sig[branch_id] = sig

    # Match signatures
    mapped = {}
    unmapped_excel = []
    unmapped_db = list(db_store_sig.keys())
    
    for st, e_sig in excel_store_sig.items():
        best_match = None
        for b_id, d_sig in db_store_sig.items():
            if e_sig == d_sig:
                best_match = b_id
                break
        
        if best_match:
            mapped[best_match] = st
            # Avoid matching multiple excel to same db
            db_store_sig.pop(best_match)
        else:
            unmapped_excel.append(st)
            
    print(f"Mapped {len(mapped)} branches successfully.")
    print(f"Unmapped Excel: {len(unmapped_excel)}")
    
    # Save the mapping to a JSON
    with open('branch_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(mapped, f, ensure_ascii=False, indent=2)
        
except Exception as e:
    print(f'Error: {e}')
