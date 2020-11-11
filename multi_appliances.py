import configparser

from utils import *
import pandas as pd
import main

FIXED_DURATION = {"dishwasher": True,
                  "washingmachine": True,
                  "microwave": False,
                  "heater": False}


def multi_appliance_build_data(appliance, config):

    data = np.zeros(main.SECOND_TENTHS_IN_A_DAY, dtype=None)

    if not is_used(appliance, config):
        return data

    series = choose_pattern(appliance, config)
    series = altering_series(series, appliance, config)
    if not FIXED_DURATION[appliance]:
        series = change_duration(series, appliance, config)

    activation_instant = choose_activation_instant(appliance, config)
    for i in range(len(series)):
        data[activation_instant + i] = series[i]

    return data


def choose_activation_instant(appliance, config):
    """
    The activation instant is chosen from a gaussian distribution where sigma is fixed for each appliance and
    mu is chosen from a uniform distribution between start and end time specified for each appliance
    """

    start = int(config['usage_start'][appliance])
    end = int(config['usage_end'][appliance])
    sigma = int(config['usage_sigma'][appliance])
    mu = np.random.randint(start, end)
    activation_instant = int(np.random.normal(mu, sigma))
    return activation_instant


def is_used(appliance, config):
    """
    There is a certain probability that an appliance is used during a day
    """

    usage_prob = float(config['usage_prob'][appliance])
    x = np.random.uniform()
    if x > usage_prob:
        return False
    return True


def choose_pattern(appliance, config):
    """
    Choosing a pattern for an appliance among the ones related to the specified model
    """

    model = config['model'][appliance]
    number_of_patterns = int(config['patterns_for_models'][appliance + str(model)])
    x = np.random.randint(1, number_of_patterns + 1)
    filename = 'data/{}/{}_house{}_{}.CSV'.format(appliance, appliance, str(model), str(x))
    series = pd.read_csv(filename, header=None, usecols=[1])[1]
    return series


def altering_series(series, appliance, config):
    """
    Each series element i is first multiplied by multiplying_factor, then is set to a value chosen whit a uniform
    distribution in the range of (series[i] +- serie[i]*noise_percentage)
    """

    multiplying_factor = float(config['multiplying_factor'][appliance])
    noise_factor = float(config['noise_percentage'][appliance])

    print(str(multiplying_factor))

    for i in range(len(series)):
        series[i] = series[i] * multiplying_factor
        series[i] = np.random.uniform(series[i] - series[i]*noise_factor,
                                      series[i] + series[i]*noise_factor)
    return series


def change_duration(series, appliance, config):
    """
    The series is expanded through interpolation of a length chosen with a uniform distribution between the min and max
    usage duration fixed for each appliance
    """

    usage_duration_min = int(config['usage_duration_min'][appliance])
    usage_duration_max = int(config['usage_duration_max'][appliance])
    usage_duration = np.random.randint(usage_duration_min, usage_duration_max)
    series = interpolate(usage_duration, len(series), series)
    return series
