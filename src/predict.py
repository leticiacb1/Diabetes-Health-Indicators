import json
import pickle
import os
import pandas as pd

def load_model(model_path: str):
    '''
    Load a trained model from a pickle file.

    :param model_path: path to the model pickle file.
    :return: loaded model
    '''
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"\n [ERROR] Model file not found: {model_path} \n")

    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)

    return model


def run(event, context):
    '''
    AWS Lambda handler function.
    Make a prediction using the trained model.

    :param event: object containing the input data
                  Expect the input to have a health_info key:
                    "health_info" : {
                                 "HighBP": ,
                                 "HighChol": ,
                                 "CholCheck":,
                                 "BMI": ,
                                 "Smoker": ,
                                 "Stroke": ,
                                 "HeartDiseaseorAttack": ,
                                 "PhysActivity": ,
                                 "Fruits": ,
                                 "Veggies" ,
                                 "HvyAlcoholConsump":,
                                 "AnyHealthcare":,
                                 "NoDocbcCost":,
                                 "GenHlth":,
                                 "MentHlth":,
                                 "PhysHlth":,
                                 "DiffWalk":,
                                 "Sex":,
                                 "Age":,
                                 "Education": ,
                                 "Income":
                                }

    :param context: AWS Lambda context object
    :return: prediction result
             (0.0 - no diabetes or 1.0 - prediabetes or diabetes)
    '''
    try:
        # Validate request
        body = event.get("body")
        if not body:
            return {
                "statusCode": 400,
                "body": json.dumps({"Error": "Invalid input: no body found."})
            }

        json_body = json.loads(body)
        health_info = json_body.get("health_info")
        if not health_info:
            return {
                "statusCode": 400,
                "body": json.dumps({"Error": "Invalid input: no 'health_info' key found in body."})
            }

        print(f"\n [INFO] Request validado.\n")
        print(f"\n [INFO] Request body : \n")
        print(f"\n        > {health_info} \n")

        # Load the model
        model_path = "logistic_regression.pickle"
        model = load_model(model_path)
        print(f"\n [INFO] Arquivo {model_path} carregado.\n")

        # Predict
        print(f"\n [INFO] Make prediction ... \n")

        feature_order = [
            "HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke",
            "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
            "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "GenHlth",
            "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income"
        ]
        features = pd.DataFrame([health_info])[feature_order]
        prediction = model.predict(features).tolist()[0]

        if(prediction == 0.0):
            condition = "no diabetes"
        else:
            condition = "prediabetes or diabetes"

        return {
            "statusCode": 200,
            "body": json.dumps({"input": health_info,"prediction": condition})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"Error": str(e)})
        }