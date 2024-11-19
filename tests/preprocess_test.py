import pytest
import pandas as pd
from io import StringIO
from preprocess import preprocess, remove_duplicate_lines, save_parquet


@pytest.fixture
def sample_csv():
    """Fixture to provide sample CSV data."""
    return StringIO("""
    id,name,age
    1,Alice,30
    2,Bob,25
    1,Alice,30
    4,Charlie,35
    2,Bob,25
    """)


@pytest.fixture
def sample_dataframe():
    """Fixture to provide sample dataframe."""
    return pd.DataFrame({
        "id": [1, 2, 1, 4, 2],
        "name": ["Alice", "Bob", "Alice", "Charlie", "Bob"],
        "age": [30, 25, 30, 35, 25]
    })


def test_remove_duplicate_lines(sample_dataframe):
    """Test remove_duplicate_lines function."""
    result = remove_duplicate_lines(sample_dataframe)

    # Check that duplicates are removed
    assert result.shape[0] == 3
    assert not result.duplicated().any()


def test_preprocess(sample_csv, tmp_path):
    """Test preprocess function."""
    # Create a temporary CSV file
    temp_file = tmp_path / "sample.csv"
    with open(temp_file, 'w') as f:
        f.write(sample_csv.getvalue())

    try:
        # Run preprocess
        processed_df = preprocess(temp_file)

        # Check the dataframe structure
        assert isinstance(processed_df, pd.DataFrame)
        assert processed_df.shape[0] == 3
    finally:
        # Clean up: delete the temporary file
        if temp_file.exists():
            temp_file.unlink()


def test_save_parquet(sample_dataframe, tmp_path):
    """Test save_parquet function."""
    # Define temporary file path
    temp_file = tmp_path / "data.parquet"

    try:
        # Save dataframe
        save_parquet(sample_dataframe, temp_file)

        # Check that the parquet file exists
        assert temp_file.exists()

        # Reload and compare data
        loaded_df = pd.read_parquet(temp_file)
        pd.testing.assert_frame_equal(sample_dataframe, loaded_df)
    finally:
        # Clean up: delete the temporary file
        if temp_file.exists():
            temp_file.unlink()
