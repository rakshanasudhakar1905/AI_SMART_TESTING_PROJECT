from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import json
from modules.test_generator import generate_test_cases
from modules.test_executor import run_tests
from modules.defect_predictor import predict_defect, train_model
app = Flask(__name__)
DATABASE = "database/database.db"
def get_db_connection():
    os.makedirs("database", exist_ok=True)
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection
def initialize_database():
    connection = get_db_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_tests INTEGER,
            passed INTEGER,
            failed INTEGER,
            errors INTEGER,
            execution_time REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS test_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id TEXT,
            test_type TEXT,
            test_case TEXT,
            expected_result TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS defect_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complexity REAL,
            changes REAL,
            previous_bugs REAL,
            lines_of_code REAL,
            test_failures REAL,
            risk TEXT,
            probability REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    connection.close()
@app.route("/")
def home():

    return render_template("index.html")
@app.route("/test-cases")
def test_cases_page():

    return render_template("test_cases.html")
@app.route("/execution")
def execution_page():

    return render_template("execution.html")

@app.route("/reports")
def reports_page():
    return render_template("reports.html")
@app.route("/api/generate-tests", methods=["POST"])
def generate_tests():

    data = request.get_json()

    requirement = data.get("requirement", "").strip()

    if not requirement:

        return jsonify({
            "success": False,
            "message": "Please enter a software requirement."
        }), 400

    test_cases = generate_test_cases(requirement)
    connection = get_db_connection()
    for test in test_cases:
        connection.execute("""
            INSERT INTO test_cases
            (test_id, test_type, test_case, expected_result)
            VALUES (?, ?, ?, ?)
        """, (
            test["id"],
            test["type"],
            test["test_case"],
            test["expected"]
        ))
    connection.commit()
    connection.close()
    return jsonify({
        "success": True,
        "count": len(test_cases),
        "test_cases": test_cases
    })
@app.route("/api/run-tests", methods=["POST"])
def execute_tests():
    result = run_tests()
    connection = get_db_connection()
    connection.execute("""
        INSERT INTO test_results
        (total_tests, passed, failed, errors, execution_time)
        VALUES (?, ?, ?, ?, ?)
    """, (
        result["total"],
        result["passed"],
        result["failed"],
        result["errors"],
        result["execution_time"]
    ))
    connection.commit()
    connection.close()
    return jsonify({
        "success": True,
        "result": result
    })
@app.route("/api/predict-defect", methods=["POST"])
def defect_prediction():
    data = request.get_json()
    try:
        complexity = float(data["complexity"])
        changes = float(data["changes"])
        previous_bugs = float(data["previous_bugs"])
        lines_of_code = float(data["lines_of_code"])
        test_failures = float(data["test_failures"])
    except (ValueError, KeyError):
        return jsonify({
            "success": False,
            "message": "Please enter valid numerical values."
        }), 400
    try:
        risk, probability = predict_defect(
            complexity,
            changes,
            previous_bugs,
            lines_of_code,
            test_failures
        )
    except FileNotFoundError:
        train_model()
        risk, probability = predict_defect(
            complexity,
            changes,
            previous_bugs,
            lines_of_code,
            test_failures
        )
    connection = get_db_connection()
    connection.execute("""
        INSERT INTO defect_predictions
        (complexity, changes, previous_bugs,
         lines_of_code, test_failures, risk, probability)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        complexity,
        changes,
        previous_bugs,
        lines_of_code,
        test_failures,
        risk,
        probability
    ))
    connection.commit()
    connection.close()
    return jsonify({
        "success": True,
        "risk": risk,
        "probability": round(probability * 100, 2)
    })
@app.route("/api/dashboard")
def dashboard_data():
    connection = get_db_connection()
    test_summary = connection.execute("""
        SELECT
            COALESCE(SUM(total_tests), 0) AS total,
            COALESCE(SUM(passed), 0) AS passed,
            COALESCE(SUM(failed), 0) AS failed,
            COALESCE(SUM(errors), 0) AS errors
        FROM test_results
    """).fetchone()
    risk_summary = connection.execute("""
        SELECT risk, COUNT(*) AS count
        FROM defect_predictions
        GROUP BY risk
    """).fetchall()
    latest_results = connection.execute("""
        SELECT *
        FROM test_results
        ORDER BY id DESC
        LIMIT 10
    """).fetchall()
    latest_predictions = connection.execute("""
        SELECT *
        FROM defect_predictions
        ORDER BY id DESC
        LIMIT 10
    """).fetchall()
    connection.close()
    risks = {
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }
    for row in risk_summary:
        if row["risk"] in risks:
            risks[row["risk"]] = row["count"]
    return jsonify({
        "tests": {
            "total": test_summary["total"],
            "passed": test_summary["passed"],
            "failed": test_summary["failed"],
            "errors": test_summary["errors"]
        },
        "risks": risks,
        "latest_results": [
            dict(row) for row in latest_results
        ],
        "latest_predictions": [
            dict(row) for row in latest_predictions
        ]
    })
if __name__ == "__main__":
    initialize_database()
    if not os.path.exists("models/defect_model.pkl"):
        train_model()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
