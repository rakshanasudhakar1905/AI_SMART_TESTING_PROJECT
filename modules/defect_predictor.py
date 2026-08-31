import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


DATA_PATH = "data/defect_data.csv"
MODEL_PATH = "models/defect_model.pkl"


def train_model():

    os.makedirs("models", exist_ok=True)

    data = pd.read_csv(DATA_PATH)

    features = [
        "complexity",
        "changes",
        "previous_bugs",
        "lines_of_code",
        "test_failures"
    ]

    X = data[features]

    y = data["defect"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    joblib.dump(model, MODEL_PATH)

    print(
        f"Defect prediction model trained. "
        f"Accuracy: {accuracy * 100:.2f}%"
    )

    return accuracy


def load_model():

    if not os.path.exists(MODEL_PATH):

        train_model()

    return joblib.load(MODEL_PATH)


def predict_defect(
    complexity,
    changes,
    previous_bugs,
    lines_of_code,
    test_failures
):

    model = load_model()

    input_data = pd.DataFrame(
        [[
            complexity,
            changes,
            previous_bugs,
            lines_of_code,
            test_failures
        ]],
        columns=[
            "complexity",
            "changes",
            "previous_bugs",
            "lines_of_code",
            "test_failures"
        ]
    )

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(
        input_data
    )[0][1]

    if probability >= 0.70:

        risk = "HIGH"

    elif probability >= 0.40:

        risk = "MEDIUM"

    else:

        risk = "LOW"

    return risk, float(probability)
