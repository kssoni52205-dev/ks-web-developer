import os
import json

from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "development-secret-change-this"
)

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get(
    "ADMIN_PASSWORD",
    "change-this-password"
)

DATA_FILE = "data.json"


def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "services": [],
            "testimonials": [],
            "contact": {
                "instagram": "",
                "phone": ""
            }
        }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


@app.route("/")
def home():

    data = load_data()

    return render_template(
        "index.html",
        data=data
    )


# =========================
# ADMIN LOGIN
# =========================

@app.route("/admin", methods=["GET", "POST"])
def admin_login():

    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            session.clear()

            session["admin_logged_in"] = True

            return redirect(
                url_for("admin_dashboard")
            )

        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template("login.html")


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    data = load_data()

    return render_template(
        "admin.html",
        data=data
    )


# =========================
# ADMIN LOGOUT
# =========================

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect(
        url_for("admin_login")
    )


# =========================
# ADD SERVICE
# =========================

@app.route(
    "/admin/service/add",
    methods=["POST"]
)
def add_service():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    data = load_data()

    service = {
        "icon": request.form.get(
            "icon",
            "🌐"
        ).strip(),

        "title": request.form.get(
            "title",
            ""
        ).strip(),

        "description": request.form.get(
            "description",
            ""
        ).strip()
    }

    if service["title"]:

        data["services"].append(service)

        save_data(data)

    return redirect(
        url_for("admin_dashboard")
    )


# =========================
# DELETE SERVICE
# =========================

@app.route(
    "/admin/service/delete/<int:index>",
    methods=["POST"]
)
def delete_service(index):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    data = load_data()

    if 0 <= index < len(data["services"]):

        data["services"].pop(index)

        save_data(data)

    return redirect(
        url_for("admin_dashboard")
    )


# =========================
# ADD TESTIMONIAL
# =========================

@app.route(
    "/admin/testimonial/add",
    methods=["POST"]
)
def add_testimonial():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    data = load_data()

    testimonial = {
        "name": request.form.get(
            "name",
            ""
        ).strip(),

        "message": request.form.get(
            "message",
            ""
        ).strip()
    }

    if (
        testimonial["name"]
        and testimonial["message"]
    ):

        data["testimonials"].append(
            testimonial
        )

        save_data(data)

    return redirect(
        url_for("admin_dashboard")
    )


# =========================
# DELETE TESTIMONIAL
# =========================

@app.route(
    "/admin/testimonial/delete/<int:index>",
    methods=["POST"]
)
def delete_testimonial(index):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    data = load_data()

    if 0 <= index < len(data["testimonials"]):

        data["testimonials"].pop(index)

        save_data(data)

    return redirect(
        url_for("admin_dashboard")
    )


# =========================
# HEALTH CHECK
# =========================

@app.route("/health")
def health():

    return {
        "status": "ok",
        "app": "KS Web Developer"
    }


# =========================
# 404 ERROR
# =========================

@app.errorhandler(404)
def page_not_found(error):

    return """
    <h1>404 - Page Not Found</h1>
    <p>The page you are looking for does not exist.</p>
    """, 404


# =========================
# RUN APP
# =========================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
