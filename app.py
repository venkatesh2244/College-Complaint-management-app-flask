import os
from cs50 import SQL
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

# Configure the Flask app
app.secret_key = "your_secret_key"


# Database connections
users_db = SQL("sqlite:///users.db")  # For users table
complaints_db = SQL("sqlite:///complaints.db")  # For complaints table


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Collect login credentials
        email = request.form.get("email")
        password = request.form.get("password")

        # Query users table for authentication
        user = users_db.execute("SELECT * FROM users WHERE email = ? AND password = ?", email, password)

        if len(user) == 1:
            # Save user session and redirect to complaints page
            session["user_id"] = user[0]["id"]
            return redirect("/complaints")
        else:
            return "Invalid email or password", 401

    return render_template("login.html")


@app.route("/complaints", methods=["GET", "POST"])
def complaints():
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    if request.method == "POST":
        # Update response in the complaints table
        complaint_id = request.form.get("complaint_id")
        response = request.form.get("response")

        complaints_db.execute(
            "UPDATE complaints SET response = ? WHERE id = ? AND user_id = ?",
            response, complaint_id, user_id,
        )

    # Fetch all complaints for the logged-in user
    complaints = complaints_db.execute("SELECT * FROM complaints WHERE user_id = ?", user_id)

    return render_template("complaints.html", complaints=complaints)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
