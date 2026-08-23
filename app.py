import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for
)

app = Flask(__name__)

# --------------------------------------------------
# SECURITY
# --------------------------------------------------

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "development-secret-change-this"
)

ADMIN_USERNAME = os.environ.get(
    "ADMIN_USERNAME",
    "admin"
)

ADMIN_PASSWORD = os.environ.get(
    "ADMIN_PASSWORD",
    "change-this-password"
)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# ADMIN LOGIN
# --------------------------------------------------

@app.route("/admin", methods=["GET", "POST"])
def admin_login():

    # Already logged in
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    # Login form submitted
    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):
            session.clear()
            session["admin_logged_in"] = True

            return redirect(url_for("admin_dashboard"))

        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template("login.html")


# --------------------------------------------------
# ADMIN DASHBOARD
# --------------------------------------------------

@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    return render_template("admin.html")


# --------------------------------------------------
# ADMIN LOGOUT
# --------------------------------------------------

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect(url_for("admin_login"))


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.route("/health")
def health():

    return {
        "status": "ok",
        "app": "KS Web Developer"
    }


# --------------------------------------------------
# ERROR HANDLERS
# --------------------------------------------------

@app.errorhandler(404)
def page_not_found(error):

    return """
    <h1>404 - Page Not Found</h1>
    <p>The page you are looking for does not exist.</p>
    """, 404


# --------------------------------------------------
# RUN APP
# --------------------------------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
