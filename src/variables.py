# Model variables
target_column_name = 'Diabetes_binary'

logistic_regression_solvers = ['lbfgs', 'liblinear', 'newton-cg', 'newton-cholesky', 'sag', 'saga']

model_path = 'models/logistic_regression.parquet'
confusion_matrix_path = 'results/confusion_matrix.png'
model_metrics_path = 'results/model_test_metrics.csv'

TEST_SIZE = 0.3
RANDOM_STATE = 1912
MAX_ITER = 1000

# Path to the data file tracked by DVC
data_path = 'data/diabetes_data.csv'

# Preprocess data path
prepro_data_path = 'data/diabetes_data.parquet'
prepro_feature_data_path = 'data/diabetes_feature_data.parquet'
prepro_target_data_path  = 'data/diabetes_target_data.parquet'

# Buckets names and keys
log_bucket_name = "mlops-project-diabetes-log-bucket"
log_preprocess_key = "mlops-project-diabetes-preprocess-logs"
log_train_key = "mlops-project-diabetes-train-logs"

# Logger
train_logger_name = "train_logger"
prepro_logger_name = "process_logger"

# MlFlow
exp_name = "mlops-project-diabetes-exp"
exp_url = "http://localhost:5000"
run_name = "project-run-v0"

# Data drift
expected_accuracy = 0.5
delta_diff = 0.1