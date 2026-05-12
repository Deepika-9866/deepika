from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "your-secret-key"  # change this

# MySQL connection (change user/password if needed)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="disaster_relief"
)
cursor = db.cursor(dictionary=True)


@app.route("/", methods=["GET", "POST"])
def index():
    # Handle SOS form submit
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        location = request.form["location"]
        help_type = request.form["help_type"]
        message = request.form["message"]

        cursor.execute(
            """
            INSERT INTO sos_requests (name, phone, location, help_type, message)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (name, phone, location, help_type, message),
        )
        db.commit()
        flash("Your request has been submitted. Help will reach you soon.")
        return redirect(url_for("index"))

    # Fetch recent requests for display
    cursor.execute(
        """
        SELECT name, phone, location, help_type, status, created_at
        FROM sos_requests
        ORDER BY created_at DESC
        LIMIT 5
        """
    )
    requests_list = cursor.fetchall()
    return render_template("indexx.html", requests_list=requests_list)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    # Update status if admin changed dropdown
    if request.method == "POST":
        req_id = request.form["id"]
        new_status = request.form["status"]
        cursor.execute(
            "UPDATE sos_requests SET status = %s WHERE id = %s",
            (new_status, req_id),
        )
        db.commit()
        flash("Request status updated.")

    # Fetch all requests for admin table
    cursor.execute(
        """
        SELECT id, name, phone, location, help_type, status, created_at
        FROM sos_requests
        ORDER BY created_at DESC
        """
    )
    all_requests = cursor.fetchall()
    return render_template("admin.html", all_requests=all_requests)


if __name__ == "__main__":
    app.run(debug=True)
