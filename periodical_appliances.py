import configparser
import numpy as np
import pandas as pd


def fridge(seconds_tenths_in_a_day):

    # Reading fridge model from configuration file
    config = configparser.ConfigParser()
    config.read('resources/config.ini')
    fridge_model = config['models']['fridge_model']

    # Reading fridge model pattern from specified model
    filename = 'data/fridge/fridge_house' + str(fridge_model) + ".CSV"
    series = pd.read_csv(filename, header=None, usecols=[1])[1]

    # Replicating fridge pattern during all day
    pattern_duration = len(series)
    pattern_in_a_day = seconds_tenths_in_a_day // pattern_duration
    data = np.zeros(seconds_tenths_in_a_day, dtype=None)
    for i in range(pattern_in_a_day):
        for j in range(pattern_duration):
            data[i * pattern_duration + j] = series[j]

    return data
