from sklearn.ensemble import RandomForestRegressor
import joblib
from src.data import load_data, split_data


def fit_model(X_train, y_train):
    """
    Train a Random Forest Regressor and save the model to a file.
    Args:
        X_train (numpy.ndarray): Training features.
        y_train (numpy.ndarray): Training target values.
    """
    # Using Random Forest for regression
    rf_regressor = RandomForestRegressor(n_estimators=100, random_state=12)
    rf_regressor.fit(X_train, y_train)

    # Ensure the '../model' directory exists or change path as needed
    joblib.dump(rf_regressor, "../model/california_model.pkl", compress=3)


if __name__ == "__main__":
    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    fit_model(X_train, y_train)