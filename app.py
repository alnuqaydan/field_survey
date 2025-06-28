from flask import Flask, jsonify, request, session
import sqlite3

app = Flask(__name__)
DB_NAME = "field_survey_production.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return "✅ Field Survey System is running!"

@app.route("/api/surveyors", methods=["GET"])
def get_surveyors():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, name, role FROM surveyors")
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/pois", methods=["GET"])
def get_pois():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM collected_pois LIMIT 10")  # جلب أول 10 فقط للتجربة
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, name, role FROM surveyors WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    conn.close()
    if user:
        return jsonify({"success": True, "user": dict(user)})
    else:
        return jsonify({"success": False, "error": "اسم المستخدم أو كلمة المرور غير صحيحة"})

if __name__ == "__main__":
    app.run(debug=True)
