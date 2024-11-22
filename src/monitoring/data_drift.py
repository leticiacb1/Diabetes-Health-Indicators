# Data
import pandas as pd
import random

# Model
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score

TEST_SIZE = 0.3
RANDOM_STATE = 1912
MAX_ITER = 1000

if __name__ == "__main__":

    # ---- Variables ----
    prepro_feature_data_path = 'data/diabetes_data.parquet'
    solver = "saga"

    expected_accuracy = 0.5
    delta_diff = 0.1

    try:
        # Prepare data for evaluation
        prepro_data = pd.read_parquet(prepro_feature_data_path)
        prepro_data_sets = prepro_data
        prepro_data_sets["Set"] = random.choices([0, 1], k=len(prepro_data_sets))

        # Split data for training
        X = prepro_data_sets.drop("Set", axis=1)
        y = prepro_data_sets["Set"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )

        # Train model
        model = LogisticRegression(solver=solver, max_iter=MAX_ITER)
        model.fit(X_train, y_train)

        # Performance
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        conf_mat = confusion_matrix(y_test, y_pred, labels=model.classes_)
        conf_mat_disp = ConfusionMatrixDisplay(
            confusion_matrix=conf_mat, display_labels=model.classes_
        )
        conf_mat_disp.plot()

        print(f"\n [INFO] Model accuracy = {accuracy} \n")

        if(abs(expected_accuracy - accuracy) <= delta_diff):
            print(f"\n [INFO] Data drift did not occur ! Accuracy = {accuracy} ")
        else:
            print(f"\n [INFO] Data drift occurred ! Accuracy = {accuracy} and is expected in range [{expected_accuracy-delta_diff} :  {expected_accuracy+delta_diff}]")

    except  Exception as e:
        # Print the error message
        print(f"\n [ERROR] An error occurred: {e}")
