import pandas as pd

def preprocess(data_path: str) -> pd.DataFrame:
    '''
    Preprocess data for model training.

    :param data_path: path to the data file tracked by DVC
    :return: dataframe with data preocessed
    '''
    df = pd.read_csv(data_path)

    # Remove duplicates rows
    prepro_df = remove_duplicate_lines(df)
    print(f" [INFO] Shape before remove duplicates = {df.shape}\n")
    print(f" [INFO] Shape after remove duplicates = {prepro_df.shape}\n")

    return prepro_df

def remove_duplicate_lines(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Remove duplicate lines in a dataframe.

    :param df: dataframe that has duplicated rows values
    :return: dataframe without duplicated rows
    '''
    n_duplicates = df.duplicated().sum()
    print(f" [INFO] Number of duplicate values = {n_duplicates}\n")
    df_no_duplicates = df.drop_duplicates()
    return df_no_duplicates

def save_parquet(df: pd.DataFrame, data_path: str) -> None:
    '''
    Save dataframe in a parquet file.

    :param df: data to be saved
    :param data_path: path for data save
    :return:
    '''
    df.to_parquet(data_path)

if __name__ == "__main__":
    # Target column
    target_column_name = 'Diabetes_binary'

    # Path to the data file tracked by DVC
    data_path = 'data/diabetes_data.csv'

    # Path to save preprocess data
    prepro_feature_data_path = 'data/diabetes_feature_data.parquet'
    prepro_target_data_path  = 'data/diabetes_target_data.parquet'

    # Preprocess data
    prepro_data = preprocess(data_path)
    features_data = prepro_data.drop(target_column_name, axis=1)
    target_data = prepro_data[target_column_name].to_frame()

    # Save preprocessed data
    save_parquet(features_data, prepro_feature_data_path)
    save_parquet(target_data, prepro_target_data_path)
