import pytest
import pandas as pd
from math import ceil

from sklearn.linear_model import LogisticRegression

import pickle

from src.train import (
    load_parquet_data, split_data, find_best_solver, train,
    save_results, save_confusion_matrix, save_model,
    TEST_SIZE, RANDOM_STATE
)

@pytest.fixture
def sample_dataframe():
    """Fixture to provide sample dataframe."""
    return pd.DataFrame({
        "feature1": [1, 2, 3, 4, 5],
        "feature2": [10, 20, 30, 40, 50],
        "target": [0, 1, 0, 1, 0]
    })

@pytest.fixture
def sample_parquet_file(tmp_path, sample_dataframe):
    """Fixture to create a sample parquet file."""
    file_path = tmp_path / "data.parquet"
    sample_dataframe.to_parquet(file_path)
    return file_path

@pytest.fixture
def logistic_solvers():
    """Fixture to provide logistic regression solvers."""
    return ["liblinear", "lbfgs"]

# Test Functions
def test_load_parquet_data(sample_parquet_file):
    """Test load_parquet_data function."""
    df = load_parquet_data(sample_parquet_file)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_split_data(sample_dataframe):
    """Test split_data function."""
    features = sample_dataframe[["feature1", "feature2"]]
    target = sample_dataframe["target"]

    # Use a fixed random state for reproducibility
    X_train, X_test, y_train, y_test = split_data(features, target)

    # Calculate expected number of samples
    expected_test_size = ceil(len(features) * TEST_SIZE)
    expected_train_size = len(features) - expected_test_size

    # Check the sizes of train and test sets
    assert len(X_train) == expected_train_size, f"Expected {expected_train_size}, got {len(X_train)}"
    assert len(X_test) == expected_test_size, f"Expected {expected_test_size}, got {len(X_test)}"

def test_find_best_solver(sample_dataframe, logistic_solvers):
    """Test find_best_solver function."""
    features = sample_dataframe[["feature1", "feature2"]]
    target = sample_dataframe["target"]

    X_train, X_test, y_train, y_test = split_data(features, target)
    best_solver = find_best_solver(logistic_solvers, X_train, y_train, X_test, y_test)

    assert best_solver in logistic_solvers

def test_train(sample_dataframe):
    """Test train function."""
    features = sample_dataframe[["feature1", "feature2"]]
    target = sample_dataframe["target"]

    X_train, _, y_train, _ = split_data(features, target)
    model = train(X_train, y_train, best_solver="liblinear")

    assert isinstance(model, LogisticRegression)

def test_save_results(sample_dataframe, tmp_path):
    """Test save_results function."""
    features = sample_dataframe[["feature1", "feature2"]]
    target = sample_dataframe["target"]

    X_train, X_test, y_train, y_test = split_data(features, target)
    model = train(X_train, y_train, best_solver="liblinear")
    y_pred = model.predict(X_test)

    results_file = tmp_path / "results.csv"
    save_results(model, results_file, y_test, y_pred)

    assert results_file.exists()

    # Reload and verify
    results_df = pd.read_csv(results_file)
    assert "Accuracy" in results_df.columns
    assert "F1" in results_df.columns

    # Cleanup
    results_file.unlink()  # Delete the file

def test_save_confusion_matrix(sample_dataframe, tmp_path):
    """Test save_confusion_matrix function."""
    features = sample_dataframe[["feature1", "feature2"]]
    target = sample_dataframe["target"]

    X_train, X_test, y_train, y_test = split_data(features, target)
    model = train(X_train, y_train, best_solver="liblinear")
    y_pred = model.predict(X_test)

    cm_file = tmp_path / "confusion_matrix.png"
    save_confusion_matrix(model, y_test, y_pred, cm_file)

    assert cm_file.exists()

    # Cleanup
    cm_file.unlink()  # Delete the file

def test_save_model(sample_dataframe, tmp_path):
    """Test save_model function."""
    features = sample_dataframe[["feature1", "feature2"]]
    target = sample_dataframe["target"]

    X_train, _, y_train, _ = split_data(features, target)
    model = train(X_train, y_train, best_solver="liblinear")

    model_file = tmp_path / "model.pkl"
    save_model(model, model_file)

    assert model_file.exists()

    # Reload and verify
    with open(model_file, "rb") as f:
        loaded_model = pickle.load(f)
    assert isinstance(loaded_model, LogisticRegression)

    # Cleanup
    model_file.unlink()
