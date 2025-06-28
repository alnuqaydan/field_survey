import sqlite3

DB_NAME = "field_survey_production.db"

tables_sql = [
    """
    CREATE TABLE IF NOT EXISTS surveyors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        name TEXT,
        password TEXT,
        role TEXT DEFAULT 'surveyor'
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        assigned_to TEXT,
        status TEXT DEFAULT 'pending'
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS collected_pois (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id TEXT,
        review_status TEXT,
        created_at TEXT,
        created_by TEXT,
        name_ar TEXT,
        name_en TEXT,
        latitude REAL,
        longitude REAL,
        operation TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS performance_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surveyor TEXT,
        date TEXT,
        points_collected INTEGER,
        quality_score REAL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS location_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surveyor TEXT,
        timestamp TEXT,
        latitude REAL,
        longitude REAL,
        accuracy REAL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS quality_checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        poi_id INTEGER,
        checked_by TEXT,
        quality_score REAL,
        notes TEXT
    );
    """
]

surveyors = [
    ("mhassanin", "محمد حسنين", "surveyor123", "surveyor"),
    ("ralhamdi",  "رياض الحمدي", "surveyor123", "surveyor"),
    ("hsamir",    "هاني سمير", "surveyor123", "surveyor"),
    ("itaher",    "إبراهيم طاهر", "surveyor123", "surveyor"),
    ("ashuban",   "أحمد شعبان", "surveyor123", "surveyor"),
    ("ralshaya",  "راشد الشايع", "surveyor123", "surveyor"),
    ("admin",     "مدير النظام", "admin123", "admin"),
    ("manager",   "مدير العمليات", "manager123", "manager"),
]

def main():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for sql in tables_sql:
        cur.execute(sql)
    conn.commit()
    for s in surveyors:
        try:
            cur.execute("INSERT OR IGNORE INTO surveyors (username, name, password, role) VALUES (?, ?, ?, ?)", s)
        except Exception as e:
            print(f"خطأ في إضافة المساح {s[0]}: {e}")
    conn.commit()
    conn.close()
    print("✅ تم إنشاء قاعدة البيانات والجداول وإدخال المساحين بنجاح!")

if __name__ == "__main__":
    main()
