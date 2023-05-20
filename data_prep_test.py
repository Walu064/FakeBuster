import pandas as pd

from samples.scripts.data_preparation import open_folder, prepare

path = "Reklamy_legit"

if __name__ == "__main__":

    paths_of_file = open_folder(path)
    # print(paths_of_file)

    df = prepare(paths_of_file)

    print(df)
