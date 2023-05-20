import pandas as pd

from samples.scripts.data_preparation import open_folder, prepare

path = "Reklamy"

if __name__ == "__main__":

    paths_of_file = open_folder(path)
    # print(paths_of_file)

    df = prepare(paths_of_file)

    if pd.read_csv('test_data.csv').empty:
        df.to_csv("test_data.csv", mode='a', header=True, index=False)
    else:
        df.to_csv("test_data.csv", mode='a', header=False, index=False)

    print(df)
