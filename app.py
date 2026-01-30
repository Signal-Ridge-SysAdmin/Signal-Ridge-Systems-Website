from flask import Flask, render_template

app = Flask(__name__)

@app.get("/")
def home():
    contact = {
        "business_name": "Signal Ridge Systems LLC",
        "city": "Gillette, WY",
        "email": "contact@signalridgesystems.com",
        "phone_display": "(307) 228-0607",
        "phone_e164": "+13072280607",
        "hours": "Mon–Fri 9am–5pm (Mountain)",
        "remote": "Remote options available",
    }
    return render_template("index.html", contact=contact)

if __name__ == "__main__":
    app.run(debug=True)
