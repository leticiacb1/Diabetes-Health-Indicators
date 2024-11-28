import pytest
import requests

from src.dataclass.gateway import Gateway
from src.dataclass.log_manager import LogManager
logger = LogManager(logger_name="gateway_test_logger")

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

    api_name = "mlops-project-diabetes-gateway"

    gateway = Gateway(logger, api_name)
    gateway._api_exists(api_name)
    endpoint = gateway.endpoint

    response = requests.post(endpoint, json=sample_input)

    assert response.status_code == 200