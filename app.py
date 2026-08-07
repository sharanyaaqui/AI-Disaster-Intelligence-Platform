from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Temporary: go to dashboard after login
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Temporary: go to login after registration
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        # Temporary: go to recommendations
        return redirect(url_for("recommendation"))
    return render_template("report.html")


@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    if request.method == "POST":
        # Temporary: reload chatbot page
        return render_template("chatbot.html")
    return render_template("chatbot.html")


@app.route("/recommendation")
def recommendation():
    return render_template("recommendation.html")


@app.route("/offline")
def offline():
    return render_template("offline.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        # Temporary: stay on profile page
        return redirect(url_for("profile"))
    return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=True)