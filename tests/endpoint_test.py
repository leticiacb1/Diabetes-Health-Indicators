import pytest
import requests
import boto3

import os
from dotenv import load_dotenv
env_filename = 'config/.env'
load_dotenv(os.path.join(os.path.dirname(__file__), env_filename))

@pytest.fixture
def sample_input():
    """Fixture to provide sample input."""
    request_body = {
        "health_info": {
            "HighBP": 0.0,
            "HighChol": 1.0,
            "CholCheck": 1.0,
            "BMI": 1.0,
            "Smoker": 40.0,
            "Stroke": 1.0,
            "HeartDiseaseorAttack": 0.0,
            "PhysActivity": 0.0,
            "Fruits": 0.0,
            "Veggies": 0.0,
            "HvyAlcoholConsump": 1.0,
            "AnyHealthcare": 0.0,
            "NoDocbcCost": 1.0,
            "GenHlth": 0.0,
            "MentHlth": 5.0,
            "PhysHlth": 18.0,
            "DiffWalk": 15.0,
            "Sex": 1.0,
            "Age": 0.0,
            "Education": 9.0,
            "Income": 4.0,
        }
    }
    return request_body


def get_api_endpoint_by_name(api_name, region):
    """
    Fetch the endpoint URL of an API Gateway by its name.

    :param api_name: Name of the API Gateway
    :param region: AWS Region
    :return: API Gateway endpoint or None if not found
    """
    client = boto3.client("apigatewayv2", region_name=region)

    try:
        response = client.get_apis()
        for api in response["Items"]:
            if api["Name"] == api_name:
                return api["ApiEndpoint"]
        print(f"[INFO] API Gateway with name '{api_name}' not found.")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to fetch API Gateway endpoint: {e}")
        return None

def test_endpoint(sample_input):
    """Test gateway and lambda function."""

    region = os.getenv("AWS_REGION")
    api_name = "mlops-project-diabetes-gateway"
    endpoint = get_api_endpoint_by_name(api_name, region)

    # Make POST request to the API Gateway endpoint
    response = requests.post(endpoint, json=sample_input)

    # Check the response
    print("\n[INFO] Sent request to API Gateway.")
    print(f"  > Endpoint: {endpoint}")
    print(f"  > Response Code: {response.status_code}")
    print(f"  > Response Body: {response.text}")

    assert response.status_code == 200