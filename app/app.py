from flask import Flask, request, render_template_string, redirect
import sqlite3
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SAFE_MODE = False  # Toggle to True for fixed version

# --- DB Setup ---
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'password123')")
    conn.commit()
    conn.close()

init_db()

# --- Vulnerable login (SQLi) ---
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        if SAFE_MODE:
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        else:
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            c.execute(query)

        user = c.fetchone()
        conn.close()

        if user:
            return redirect("/dashboard")
        else:
            return "Invalid login!"

    return """
    <form method="POST">
      Username: <input name="username"><br>
      Password: <input name="password" type="password"><br>
      <input type="submit" value="Login">
    </form>
    """

# --- XSS vulnerable comments ---
comments = []
@app.route("/comments", methods=["GET", "POST"])
def comment():
    global comments
    if request.method == "POST":
        msg = request.form["msg"]
        comments.append(msg)
    return render_template_string("""
    <form method="POST">
      <input name="msg">
      <input type="submit" value="Post">
    </form>
    <h3>Comments:</h3>
    {% for c in comments %}
        <p>{{c|safe}}</p>
    {% endfor %}
    """, comments=comments)

# --- File Upload ---
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        return f"Uploaded to {filepath}"
    return """
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    """

@app.route("/dashboard")
def dashboard():
    return "<h1>Welcome to the Dashboard (vulnerable)</h1>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
