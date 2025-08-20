# Vulnerabilities\n\n1. SQL Injection\n2. XSS\n3. Unsafe File Upload

# Vulnerabilities Documentation – My Web Vuln Lab

This document contains step-by-step exploitation and explanation for all vulnerabilities in the custom Flask web app.

---

## 1️⃣ SQL Injection (Login)

**Route:** `/login`  
**Vulnerability:** SQL Injection in login query.

**Exploit Steps:**
1. Open the app: `http://127.0.0.1:5000`
2. Enter the following credentials:
   - **Username:** `admin' OR '1'='1`
   - **Password:** anything
3. Click **Login** → you should be logged in without knowing the real password.

**Screenshot:**  
 ![SQL Injection](https://github.com/user-attachments/assets/8479fabc-9640-4055-8fdd-14eaea766c8c)


**Impact:**  
- Bypasses authentication.
- Attacker can log in as any user without credentials.

**Fix Recommendation:**  
- Use parameterized queries / prepared statements:

python
cur.execute("SELECT id, username FROM users WHERE username=? AND password=?, (u, p))


##  2️⃣ Cross-Site Scripting (XSS)

Route: /comments
Vulnerability: Stored XSS via comments form.

Exploit Steps:

Go to http://127.0.0.1:5000/comments

Post a comment:
<script>alert('xss')</script>

3.Submit → an alert box should pop up.

Screenshot:
![XSS](https://github.com/user-attachments/assets/a8f6ae03-5d62-41f2-9855-403cf0fbc2b9)
![XSSp2](https://github.com/user-attachments/assets/068b89ff-431d-41e0-ba05-a925b4ef1237)


Impact:

Executes arbitrary JavaScript in users’ browsers.

Could steal cookies, session tokens, or redirect users.

Fix Recommendation:

Escape user input or remove |safe in template.

Implement Content Security Policy (CSP).


3️⃣ Unsafe File Upload

Route: /upload
Vulnerability: Upload any file without validation.

Exploit Steps:

Create a file test.html with content:

<h1>Owned!</h1>
<script>alert('uploaded-xss')</script>

Go to http://127.0.0.1:5000/upload

Upload test.html

Click the uploaded file link → the alert should fire.

Screenshot:

![Upload](https://github.com/user-attachments/assets/ea2bc614-ac1c-4551-bd3f-9209b4dcebbf)

Impact:

Can upload malicious scripts.

Potential remote code execution if served improperly.

Fix Recommendation:

Validate file extensions & MIME type.

Store files outside the web root.

Randomize filenames.

