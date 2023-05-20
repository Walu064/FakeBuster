from samples.scripts.data_preparation import open_folder, prepare

path = "Reklamy"

if __name__ == "__main__":

    paths_of_file = open_folder(path)
    # print(paths_of_file)

    df = prepare(paths_of_file)

    df.to_csv("test_data.csv", index=False)

    print(df)
