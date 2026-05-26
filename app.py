from flask import Flask
from config import Config
from models import db
from routes import register_routes
from flask import render_template, request, redirect
from werkzeug.utils import secure_filename
import os

import requests
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

register_routes(app)


# =========================
# KEEP ALIVE ROUTE
# =========================

@app.route("/ping")
def ping():
    return "OK"


# =========================
# SELF PING FUNCTION
# =========================

def self_ping():
    try:
        requests.get(
            "https://go-gas-bihc.onrender.com/ping"
        )
    except:
        pass


# =========================
# START SCHEDULER
# =========================

scheduler = BackgroundScheduler()

scheduler.add_job(
    self_ping,
    "interval",
    minutes=10
)

scheduler.start()


# =========================
# RUN APP
# =========================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host='0.0.0.0',
        port=port
    )
