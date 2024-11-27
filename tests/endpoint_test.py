import pytest
import requests

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

def test_endpoint(sample_input):
    """Test gateway and lambda function."""

    # API URL = https://<API_GATEWAY_ID>.execute-api.<REGION>.amazonaws.com/<ROUTE>
    endpoint = "https://gn5battgc1.execute-api.us-east-2.amazonaws.com/predict"

    # Make POST request to the API Gateway endpoint
    response = requests.post(endpoint, json=sample_input)

    # Check the response
    print("\n[INFO] Sent request to API Gateway.")
    print(f"  > Endpoint: {endpoint}")
    print(f"  > Response Code: {response.status_code}")
    print(f"  > Response Body: {response.text}")

    assert response.status_code == 200