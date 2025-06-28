import sqlite3
import pandas as pd
import glob

DB_NAME = "field_survey_production.db"

def load_all_csv_files():
    files = glob.glob("poi_data_part_*.csv")
    if not files:
        print("❌ لم يتم العثور على أي ملفات بيانات")
        return None
    dataframes = [pd.read_csv(file) for file in files]
    df = pd.concat(dataframes, ignore_index=True)
    print(f"✅ تم دمج {len(files)} ملف. مجموع النقاط: {len(df)}")
    return df

def main():
    df = load_all_csv_files()
    if df is None:
        return

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO collected_pois (
                transaction_id, review_status, created_at, created_by,
                name_ar, name_en, latitude, longitude, operation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(row.get('transaction_id', '')),
            str(row.get('review_status', 'draft')),
            str(row.get('created_at', '')),
            str(row.get('created_by', '')),
            str(row.get('name_ar', '')),
            str(row.get('name_en', '')),
            float(row.get('latitude', 0)),
            float(row.get('longitude', 0)),
            str(row.get('operation', 'create')),
        ))
    conn.commit()
    conn.close()
    print(f"✅ تم تحميل البيانات بنجاح إلى قاعدة البيانات! عدد النقاط: {len(df)}")

if __name__ == "__main__":
    main()
