# Data
import pandas as pd

# Variables
from src.variables import target_column_name, logistic_regression_solvers, \
                      model_path, confusion_matrix_path, model_metrics_path, \
                      TEST_SIZE, RANDOM_STATE, MAX_ITER, \
                      prepro_feature_data_path, prepro_target_data_path, \
                      log_bucket_name, log_train_key, \
                      exp_name, exp_url, run_name, \
                      train_logger_name

# Export
import pickle

# Plot
import matplotlib.pyplot as plt
import seaborn as sns

# Model
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, mean_absolute_error, mean_squared_error, r2_score

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Logging
from src.dataclass.bucket.log_bucket import LogBucket
from src.dataclass.log_manager import LogManager
logger = LogManager(logger_name = train_logger_name)

# Tracking
import mlflow

def load_parquet_data(file_path: str) -> pd.DataFrame:
    '''
    Load data from .parquet file.

    :param file_path: location where the file will be saved
    :return: dataframe with file content
    '''
    df = pd.read_parquet(file_path)

    logger.log.debug(f" [DEBUG] Load file = {file_path} \n")

    return df

def split_data(features_data: pd.DataFrame, target_date: pd.Series) -> (pd.DataFrame, pd.DataFrame, pd.Series, pd.Series):
    '''
    Split data for training.

    :param features_data: dataframe with features values
    :param target_date: series with target values
    :return: split data
    '''
    X_train, X_test, y_train, y_test = train_test_split(
        features_data, target_date, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    logger.log.info(f" [INFO] Split data for training \n")

    return X_train, X_test, y_train, y_test


def find_best_solver(logistic_regression_solvers, X_train, y_train, X_test, y_test) -> str :
    '''
    Find the best solver for Logistic Regression

    :param logistic_regression_solvers: list with logistic regression solvers
    :param X_train: dataframe with feature value from training set
    :param y_train: series with the train set target values
    :param X_test: dataframe with feature value from test set
    :param y_test: series with the test set target values
    :return: best solver obtained
    '''
    # Default
    best_solver = logistic_regression_solvers[0]

    # Map solver with init scores
    train_score_values = {}
    for solver in logistic_regression_solvers:
        train_score_values[solver] = 0

    # Find best solver score
    for solver in logistic_regression_solvers:
        model = LogisticRegression(solver=solver).fit(X_train, y_train)
        train_score_values[solver] = model.score(X_test, y_test)

        if train_score_values[solver] >= max(train_score_values.values()):
            best_solver = solver

    logger.log.info(f" [INFO] The best solver find for Logistic Regression model was : {best_solver} \n")

    return best_solver


def train(X_train: pd.DataFrame, y_train: pd.Series, best_solver: str):
    '''
    Train Logistic Regression Model.

    :param X_train: dataframe with feature value from training set
    :param y_train: series with the train set target values
    :return: Logistic Regression Model
    '''
    model = LogisticRegression(solver=best_solver, max_iter=MAX_ITER)
    model.fit(X_train, y_train)

    logger.log.info(f" [INFO] Training Logistic Regression model with {best_solver} solver \n")

    mlflow.log_param("max_iter", MAX_ITER)
    mlflow.log_param("best_solver", best_solver)
    signature = mlflow.models.signature.infer_signature(
        X_train, model.predict(X_train)
    )
    mlflow.sklearn.log_model(
        model,
        "logistic_regression_model",
        signature=signature,
        registered_model_name="logistic_regression-model",
        input_example=X_train.iloc[:3],
    )

    return model

def save_results(model, file_path: str, y_test: pd.Series, y_pred: pd.Series) -> None:
    '''
    Save performance results in a file_path

    :param model: model used in training
    :param file_path: path where the results will be saved
    :param y_test: series with the test set target values
    :param y_pred: series with the values predicted by the model
    :return: None
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

    logger.log.info(f" [INFO] Saving model performance results at {file_path}: \n")
    logger.log.info(f" [INFO] Accuracy = {accuracy}; F1 = {f1}; MAE= {mae}; MSE= {mse}; R2:{r2}  \n")

    mlflow.log_metric("Accuracy", accuracy)
    mlflow.log_metric("F1", f1)
    mlflow.log_metric("MAE", mae)
    mlflow.log_metric("MSE", mse)
    mlflow.log_metric("R2", r2)

def save_confusion_matrix(model, y_test: pd.Series, y_pred: pd.Series, file_path: str) -> None:
    '''
    Save model confusion matrix.

    :param model: model used in training
    :param y_test: series with the test set target values
    :param y_pred: series with the values predicted by the model
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
    plt.savefig(file_path)
    plt.close()

    logger.log.info(f" [INFO] Saving confusion matrix at {file_path} \n")
    mlflow.log_artifact(file_path)

def save_model(model, file_path: str) -> None:
    '''
    Save model in a .pickle file.

    :param model: model used in training
    :param file_path: location where the file will be saved
    :return: None
    '''
    with open(file_path, "wb") as f:
        pickle.dump(model, f)

    logger.log.info(f" [INFO] Saving model file at {file_path} \n")

if __name__ == "__main__":

    mlflow.set_tracking_uri(exp_url)
    mlflow.set_experiment(exp_name)
    with mlflow.start_run():
        mlflow.set_tag("mlflow.runName", run_name)

        try:
            # Load preprocess data
            df_features = load_parquet_data(prepro_feature_data_path)
            df_target = load_parquet_data(prepro_target_data_path)

            # Split data
            X_train, X_test, y_train, y_test = split_data(df_features, df_target[target_column_name])

            # Train model
            best_solver = find_best_solver(logistic_regression_solvers, X_train, y_train, X_test, y_test)
            logistic_regression_model = train(X_train, y_train, best_solver)

            # Predict
            y_pred = logistic_regression_model.predict(X_test)

            # Save
            save_model(logistic_regression_model, model_path)
            save_confusion_matrix(logistic_regression_model, y_test, y_pred, confusion_matrix_path)
            save_results(logistic_regression_model, model_metrics_path, y_test, y_pred)
        except Exception as e:
            logger.log.error(f" [ERROR] An error occurred: {e} \n")
        finally:
            # Write Logs in S3 bucket
            log_bucket = LogBucket(logger, log_bucket_name)
            log_bucket.create()
            log_bucket.write_logs(logger.string_io.getvalue(), log_train_key)

            # Check logs:
            # log_bucket.check_content()
            # log_bucket.read_logs(log_key)

            logger.log.info(f" [INFO] MLFlow {exp_name}  running at: {exp_url} \n")