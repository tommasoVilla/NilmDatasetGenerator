import configparser

import numpy as np
import pandas as pd
import main
from utils import altering_series


def periodical_appliance_build_data(appliance, config):
    """
    After the reading of the unique pattern, this function calculate how many times the pattern fits in a day and
    generate data reproducing that patter all day long
    """

    model = config['model'][appliance]
    filename = 'data/{}/{}_house{}.CSV'.format(appliance, appliance, str(model))
    series = pd.read_csv(filename, header=None, usecols=[1])[1]
    pattern_duration = len(series)
    pattern_in_a_day = main.SECOND_TENTHS_IN_A_DAY // pattern_duration
    data = np.zeros(main.SECOND_TENTHS_IN_A_DAY, dtype=None)

    for i in range(pattern_in_a_day):
        for j in range(pattern_duration):
            data[i * pattern_duration + j] = series[j]

    data = altering_series(data, appliance, config)

    return data
