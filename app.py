"""Signal Ridge Systems LLC website (Flask)."""

import os
import smtplib
from email.message import EmailMessage
from datetime import datetime, timezone

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

# Needed for flash() messages. Set FLASK_SECRET_KEY in your environment for production.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-change-me")

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


def send_contact_email(payload: dict) -> None:
    """Send a contact-form submission to the business inbox, BCC founder."""
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))

    smtp_user = os.environ["SMTP_USER"]  # e.g. info@signalridgesystems.dev
    smtp_pass = os.environ["SMTP_PASS"]  # Google Workspace app password

    to_addr = os.environ.get("CONTACT_TO", "info@signalridgesystems.dev")
    bcc_addr = os.environ.get("CONTACT_BCC", "william.zade@signalridgesystems.dev")

    msg = EmailMessage()
    msg["Subject"] = f"New Contact Request — {payload['topic']}"
    msg["From"] = smtp_user
    msg["To"] = to_addr
    msg["Bcc"] = bcc_addr

    # When you hit reply, it replies to the customer.
    msg["Reply-To"] = payload["email"]

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    body = f"""New message from the website contact form

Name: {payload['name']}
Email: {payload['email']}
Phone: {payload.get('phone','')}
Topic: {payload['topic']}

Message:
{payload['message']}

---
Time: {ts}
IP: {payload.get('ip','')}
User-Agent: {payload.get('ua','')}
"""
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)


@app.get("/")
def home():
    return render_template("index.html", contact=CONTACT, active_page="home")


@app.get("/services")
def services():
    return render_template("services.html", contact=CONTACT, active_page="services")


@app.get("/links")
def links():
    return render_template("links.html", contact=CONTACT, active_page="links")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Honeypot: bots fill; humans never see it
        if request.form.get("company"):
            flash("Thanks — message received. I’ll get back to you soon.", "success")
            return redirect(url_for("contact"))

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        topic = request.form.get("topic", "").strip()
        message = request.form.get("message", "").strip()

        if not (name and email and topic and message):
            flash("Please fill out the required fields.", "error")
            return redirect(url_for("contact"))

        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            "topic": topic,
            "message": message,
            "ip": request.headers.get("X-Forwarded-For", request.remote_addr),
            "ua": request.headers.get("User-Agent", ""),
        }

        try:
            send_contact_email(payload)
            flash("Thanks — message received. I’ll get back to you soon.", "success")
        except Exception:
            flash(
                "Sorry — something went wrong sending your message. Please email info@signalridgesystems.dev.",
                "error",
            )

        return redirect(url_for("contact"))

    return render_template("contact.html", contact=CONTACT, active_page="contact")


if __name__ == "__main__":
    app.run(debug=True)
