print("TRAIN STARTED")

import os
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report

MODEL_PATH = "models/model.pkl"

def main():
    print("MAIN RUNNING")

    iris = load_iris()
    X, y = iris.data, iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("svc", SVC())
    ])

    param_grid = {
        "svc__C": [0.1, 1, 10],
        "svc__gamma": ["scale", "auto"],
        "svc__kernel": ["linear", "rbf"]
    }

    grid = GridSearchCV(
        pipeline,
        param_grid,
        cv=5,
        scoring="accuracy",
        n_jobs=-1
    )

    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_

    y_pred = best_model.predict(X_test)
    print("Best params:", grid.best_params_)
    print(classification_report(y_test, y_pred, target_names=iris.target_names))

    os.makedirs("models", exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(best_model, f)

    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    main()
