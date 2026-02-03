"""Signal Ridge Systems LLC website (Flask)."""

from flask import Flask, render_template

app = Flask(__name__)

# Shared contact info for all pages
CONTACT = {
    "business_name": "Signal Ridge Systems LLC",
    "city": "Gillette, WY",
    "email": "info@signalridgesystems.dev",
    "phone_display": "(307) 228-0607",
    "phone_e164": "+13072280607",
    "hours": "Mon–Fri 9am–5pm (Mountain)",
    "remote": "Remote options available",
}


@app.get("/")
def home():
    """Render the homepage."""
    return render_template("index.html", contact=CONTACT, active_page="home")


@app.get("/services")
def services():
    """Render the services page."""
    return render_template("services.html", contact=CONTACT, active_page="services")


@app.get("/about")
def about():
    """Render the about page."""
    return render_template("about.html", contact=CONTACT, active_page="about")


@app.get("/contact")
def contact():
    """Render the contact page."""
    return render_template("contact.html", contact=CONTACT, active_page="contact")


if __name__ == "__main__":
    app.run(debug=True)
