import os
import glob
import pandas as pd


def remove_absolute_paths(path, dataframe):
    """ Removes any absolute paths in favor of relative ones
    """
    for i, row in dataframe.iterrows():
        right, left, center = dataframe.loc[i, 'right'], dataframe.loc[i, 'left'], dataframe.loc[i, 'center']
        corrected_r = os.path.join(path, os.path.split(right)[-1])
        corrected_l = os.path.join(path, os.path.split(left)[-1])
        corrected_c = os.path.join(path, os.path.split(center)[-1])
        dataframe.set_value(i, 'right', corrected_r)
        dataframe.set_value(i, 'left', corrected_l)
        dataframe.set_value(i, 'center', corrected_c)


def read_csv(p):
    sep = ','
    names = ['center', 'left', 'right', 'steer', 'throttle', 'brake', 'speed']
    return pd.read_csv(p, sep=sep, names=names)


def create_appended_log(path):
    """ Out of all csv files generated with the correct relative paths
        generate one with one header
    """
    all_files = glob.glob(path + "/*.csv")
    df_from_each_file = (read_csv(f) for f in all_files)
    concatenated_df = pd.concat(df_from_each_file).drop_duplicates().reset_index(drop=True)
    concatenated_df.to_csv(os.path.join(path, 'driving_log_compiled.csv'), header=False, index=False)


def gather_data(path):
    """ Navigate through a driving_log.csv files under
        data directory and compile into one massive csv file
    """
    def get_paths(p):
        return [os.path.join(p, t) for t in os.listdir(p)]

    tracks = get_paths(path)
    datasets = [get_paths(track) for track in tracks]
    datasets = [d for track in datasets for d in track]
    log_file_name = 'driving_log.csv'
    for i, dataset in enumerate(datasets):
        df = read_csv(os.path.join(dataset, log_file_name))
        remove_absolute_paths(dataset, df)
        csv_name = 'driving_log_compiled_{index}.csv'.format(index=i)
        df.to_csv(os.path.join(path, csv_name), index=False)
        print("Saved: ", dataset, "to: ", csv_name)
    return datasets


def get_file(data_path):
    """ Check that driving_log_compiled.csv is a valid File
        returns: (isFileFlag, os.path to file)
    """
    file = os.path.join(data_path, 'driving_log_compiled.csv')
    return os.path.isfile(file), file


def data_validation(path='./data'):
    """ Check that the centralized csv is there, create if not
        returns: os.path to the file
    """
    is_data_gathered, file = get_file(path)
    if not is_data_gathered:
        datasets = gather_data(path)
        create_appended_log(path)
        print("Data gathered from ",  datasets)
    else:
        print("Concatenated CSV File exists")
    return file


def test():
    path = '../data'
    assert(os.path.isfile(data_validation(path)))


if __name__ == '__main__':
    test()
