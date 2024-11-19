# Data
import pandas as pd

# Export
import pickle

# Plot
import matplotlib.pyplot as plt
import seaborn as sns

# Modeling
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


TEST_SIZE = 0.3
RANDOM_STATE = 1912

def load_data(data_path: str) -> pd.DataFrame:
    '''
    Load data from .parquet file.

    :param data_path: path where the file is located
    :return: dataframe with file content
    '''
    df = pd.read_parquet(data_path)
    return df

def split_data(features_data: pd.DataFrame, target_date: pd.Series) -> (pd.DataFrame, pd.DataFrame, pd.Series, pd.Series):
    '''
    Split data for training.

    :param features_data: dataframe with features values
    :param target_date: series with target values
    :return: data splited
    '''
    X_train, X_test, y_train, y_test = train_test_split(
        features_data, target_date, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    return X_train, X_test, y_train, y_test


def find_best_model_solver(logistic_regression_solvers, X_train, y_train, X_test, y_test):
    '''

    :param logistic_regression_solvers:
    :param X_train:
    :param y_train:
    :param X_test:
    :param y_test:
    :return:
    '''
    train_score_values = {}
    best_slover = ''

    for i, n in enumerate(logistic_regression_solvers):
        model = LogisticRegression(solver=n).fit(X_train, y_train)
        train_score_values[n] = model.score(X_test, y_test)

        if train_score_values[n] >= max(train_score_values.values()):
            best_slover = n

    return best_slover, train_score_values


def train(X_train: pd.DataFrame, y_train: pd.Series, best_solver: str):
    '''
    Train Logistic Regression Model.

    :param X_train: dataframe with features value for train
    :param y_train: series with target values for train
    :return: Logistic Regression Model
    '''
    model = LogisticRegression(solver=best_solver)
    model.fit(X_train, y_train)
    return model

def save_results(model, file_path: str, y_test: pd.Series, y_pred: pd.Series) -> None:
    '''

    :param model:
    :param file_path:
    :param y_test:
    :param y_pred:
    :return:
    '''
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Create a DataFrame with the evaluation metrics
    results_df = pd.DataFrame(
        {"Accuracy": [accuracy], "F1": [f1], "MAE": [mae], "MSE": [mse], "R2":[r2]}
    )

    results_df.to_csv(file_path, index=False)

def save_confusion_matrix(model, y_test: pd.Series, y_pred: pd.Series) -> None:
    '''

    :param model:
    :param y_test:
    :param y_pred:
    :return:
    '''
    cm = confusion_matrix(y_test, y_pred)

    # Create a pandas DataFrame for the confusion matrix
    cm_df = pd.DataFrame(cm, index=model.classes_, columns=model.classes_)

    # Generate the confusion matrix plot
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm_df, annot=True, cmap="Blues")
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted Labels")
    plt.ylabel("True Labels")
    plt.savefig("results/confusion_matrix.png")
    plt.close()

def save_model(model, file_path: str) -> None:
    '''
    Save model in a .pickle file.

    :param model: Model used for training.
    :param file_path: Path wher model will be saved
    :return: None
    '''
    with open(file_path, "wb") as f:
        pickle.dump(model, f)

if __name__ == "__main__":
    pass
    # df = load_data()
    # X_train, X_test, y_train, y_test = split(df)
    # ohe = train_ohe(X_train)
    # X_train = ohe.transform(X_train)
    # X_test = ohe.transform(X_test)
    #
    # model = train(X_train, y_train)
    # y_pred = model.predict(X_test)
    #
    # export_results(model, X_test, y_test, y_pred)
    # export_confusion_matrix(model, y_test, y_pred)
    # export_model(ohe, "models/ohe.pickle")
    # export_model(model, "models/model.pickle")