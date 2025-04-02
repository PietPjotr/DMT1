import pandas as pd


def get_all_user_ids(df):
    ids = set([ID for ID in df['id']])
    return sorted([int(el[-2:]) for el in ids])


def load_csv(file_path):
    """Loads the CSV file into a Pandas DataFrame."""
    df = pd.read_csv(file_path, index_col=0)  # Ignore the unnamed index column
    return df


def filter(df, cols, values):
    
    df.loc[(df['column_name'] >= A) & (df['column_name'] <= B)]


# Example usage:
df = load_csv("dataset_mood_smartphone.csv")
ids = get_all_user_ids(df)
print(ids)

# user_data = get_user_data(df, 3)
# print(user_data)
