# Data
import pandas as pd
from pandas.io.xml import preprocess_data

# Logging
from src.dataclass.bucket.log_bucket import LogBucket
from src.dataclass.log_manager import LogManager
logger = LogManager(logger_name = "process_logger")

def preprocess(data_path: str) -> pd.DataFrame:
    '''
    Preprocess data for model training.

    :param data_path: path to the data file tracked by DVC
    :return: dataframe with data preocessed
    '''
    df = pd.read_csv(data_path)

    # Remove duplicates rows
    prepro_df = remove_duplicate_lines(df)

    logger.log.info(f" [INFO] Shape before remove duplicates = {df.shape}\n")
    logger.log.info(f" [INFO] Shape after remove duplicates = {prepro_df.shape}\n")

    return prepro_df

def remove_duplicate_lines(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Remove duplicate lines in a dataframe.

    :param df: dataframe that has duplicated rows values
    :return: dataframe without duplicated rows
    '''
    n_duplicates = df.duplicated().sum()
    df_no_duplicates = df.drop_duplicates()

    logger.log.info(f" [INFO] Removing duplicated lines : {n_duplicates} duplicate rows \n")

    return df_no_duplicates

def save_parquet(df: pd.DataFrame, data_path: str) -> None:
    '''
    Save dataframe in a parquet file.

    :param df: data to be saved
    :param data_path: path for data save
    :return:
    '''
    df.to_parquet(data_path)

    logger.log.info(f" [INFO] Saving the preprocess data at {data_path} \n")

if __name__ == "__main__":

    # ---- Variables ----
    target_column_name = 'Diabetes_binary'

    data_path = 'data/diabetes_data.csv' # Path to the data file tracked by DVC

    prepro_data_path = 'data/diabetes_data.parquet'
    prepro_feature_data_path = 'data/diabetes_feature_data.parquet'
    prepro_target_data_path  = 'data/diabetes_target_data.parquet'

    log_bucket_name = "mlops-project-diabetes-log-bucket"
    log_key = "mlops-project-diabetes-preprocess-logs"

    # ---- Main ----
    try:
        # Preprocess data
        prepro_data = preprocess(data_path)
        features_data = prepro_data.drop(target_column_name, axis=1)
        target_data = prepro_data[target_column_name].to_frame()

        # Save preprocessed data
        save_parquet(prepro_data, prepro_data_path)
        save_parquet(features_data, prepro_feature_data_path)
        save_parquet(target_data, prepro_target_data_path)

    except Exception as e:
        logger.log.error(f" [ERROR] An error occurred: {e} \n")
    finally:
        # Write Logs in S3 bucket
        log_bucket = LogBucket(logger, log_bucket_name)
        log_bucket.create()
        log_bucket.write_logs(logger.string_io.getvalue(), log_key)

        # Check logs:
        # log_bucket.check_content()
        # log_bucket.read_logs(log_key)