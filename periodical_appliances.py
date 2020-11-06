import configparser
import numpy as np
import pandas as pd


def fridge(seconds_tenths_in_a_day):

    config = configparser.ConfigParser()
    config.read('resources/config.ini')
    fridge_model = config['models']['fridge_model']
    filename = 'data/fridge/fridge_house' + str(fridge_model) + ".CSV"

    # 6932 rows has to be skipped to concat pattern cleanly
    series = pd.read_csv(filename, header=None, usecols=[1], skiprows=6932)[1]

    pattern_duration = len(series)
    pattern_in_a_day = seconds_tenths_in_a_day // pattern_duration

    data = np.zeros(seconds_tenths_in_a_day, dtype=None)

    for i in range(pattern_in_a_day - 1):
        for j in range(pattern_duration - 1):
            data[i * pattern_duration + j] = series[j]

    return data
