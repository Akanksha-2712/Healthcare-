import sqlite3
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)
DATABASE_PATH = Path(__file__).resolve().parent / "healthcare.db"


def initialize_database():
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                service TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                symptoms TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


initialize_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check_symptoms():
    symptom = request.form.get("symptom", "").lower()

    if "fever" in symptom:
        result = "You may have a fever. Take adequate rest and stay hydrated."
    elif "headache" in symptom:
        result = "For a mild headache, rest and drink enough water. Consult a doctor if it continues."
    elif "cold" in symptom or "cough" in symptom:
        result = "You may have common cold symptoms. Rest and stay hydrated."
    else:
        result = "We could not identify the symptom. Please consult a qualified healthcare professional."

    return render_template("index.html", result=result)


@app.route("/appointment", methods=["POST"])
def appointment():
    appointment_data = (
        request.form["name"].strip(),
        request.form["age"],
        request.form["gender"],
        request.form["email"].strip(),
        request.form["phone"].strip(),
        request.form["doctor"],
        request.form["date"],
        request.form.get("symptoms", "").strip(),
    )

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            INSERT INTO appointments (
                name, age, gender, email, phone, service, appointment_date, symptoms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            appointment_data,
        )

    message = (
        f"Appointment request received for {appointment_data[0]} "
        f"on {appointment_data[6]}."
    )

    return render_template(
        "index.html",
        appointment_message=message
    )


if __name__ == "__main__":
    app.run(debug=True)