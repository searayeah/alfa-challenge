import pickle

import pandas as pd


def reduce_df_size(
    df: pd.DataFrame, force_cat: list | None = None, drop: list | None = None
) -> pd.DataFrame:

    start_mem = df.memory_usage().sum() / 1024**2
    print(f"Memory usage of dataframe is {start_mem:.2f} MB")

    # drops
    if drop:
        for drop_col in drop:
            df = df.drop(drop_col, axis=1)

    float_columns = df.select_dtypes("float").columns
    integer_columns = df.select_dtypes("integer").columns

    # for float all are possible from float to unsigned
    df[float_columns] = df[float_columns].apply(pd.to_numeric, downcast="float")
    df[float_columns] = df[float_columns].apply(pd.to_numeric, downcast="integer")
    df[float_columns] = df[float_columns].apply(pd.to_numeric, downcast="unsigned")

    # for integer two possibilities
    df[integer_columns] = df[integer_columns].apply(pd.to_numeric, downcast="integer")
    df[integer_columns] = df[integer_columns].apply(pd.to_numeric, downcast="unsigned")

    # category
    if force_cat:
        for category_col in force_cat:
            df[category_col] = df[category_col].astype("category")

    end_mem = df.memory_usage().sum() / 1024**2
    print(f"Memory usage after optimization is: {end_mem:.2f} MB")
    print(f"Decreased by {100 * (start_mem - end_mem) / start_mem:.1f}%")
    return df


def cache_or_generate(filename, generator_function, load, *args, **kwargs):
    if load:
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                print(f"Loading data from {filename}")
                return pickle.load(f)
        else:
            print(f"Generating and saving data to {filename}")
            data = generator_function(*args, **kwargs)
            with open(filename, "wb") as f:
                pickle.dump(data, f)
            return data
    else:
        print("Not loading")
        return None
