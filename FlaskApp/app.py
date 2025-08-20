from flask import Flask, request, redirect, render_template
import mysql.connector
from config.db_config import DB_CONFIG

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/")
def index():
    return "<h1>Hello, Welcome to your list!</h1>"

@app.route("/add", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        content = request.form["content"]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (content) VALUES (%s)", (content,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/show")
    return render_template("add.html")

@app.route("/show")
def show_items():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("show.html", items=items)

@app.route("/delete/<int:item_id>")
def delete_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/show")

if __name__ == "__main__":
    init_db()
    app.run(debug=True,host='0.0.0.0')
