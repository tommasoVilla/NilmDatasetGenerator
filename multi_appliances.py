import configparser
import numpy as np
import pandas as pd
from utils import *


def dishwasher(seconds_tenths_in_a_day):
    config = configparser.ConfigParser()
    config.read('resources/config.ini')
    data = np.zeros(seconds_tenths_in_a_day, dtype=None)

    # With a certain probability dishwasher is not used during this day
    dishwasher_usage_prob = float(config['usage_probabilities']['dishwasher_usage_prob'])
    x = np.random.uniform()
    if x > dishwasher_usage_prob:
        return data

    # Reading dishwasher model from configuration file
    dishwasher_model = config['models']['dishwasher_model']

    # Reading the number of possible pattern for the specified model
    dishwasher_patterns = int(config['patterns_for_models']['dishwasher' + str(dishwasher_model)])

    # Select a random pattern between those available and building the corresponding series
    x = np.random.randint(1, dishwasher_patterns + 1)
    filename = 'data/dishwasher/dishwasher_house' + str(dishwasher_model) + "_" + str(x) + ".CSV"
    series = pd.read_csv(filename, header=None, usecols=[1])[1]

    # Altering series
    dishwasher_factor = float(config['alterations']['dishwasher_factor'])
    dishwasher_noise_factor = float(config['alterations']['dishwasher_noise_factor'])
    for i in range(len(series)):
        series[i] = series[i] * np.random.uniform(dishwasher_factor - dishwasher_noise_factor,
                                                  dishwasher_factor + dishwasher_noise_factor)

    # Choosing a start instant
    dishwasher_start = int(config['usage_start']['dishwasher_start'])
    dishwasher_end = int(config['usage_start']['dishwasher_end'])
    mu = np.random.randint(dishwasher_start, dishwasher_end)
    sigma = int(config['usage_start']['dishwasher_sigma'])
    activation_instant = int(np.random.normal(mu, sigma))

    # Building dishwasher data
    for i in range(len(series)):
        data[activation_instant + i] = series[i]

    return data


def washingmachine(seconds_tenths_in_a_day):
    config = configparser.ConfigParser()
    config.read('resources/config.ini')
    data = np.zeros(seconds_tenths_in_a_day, dtype=None)

    # With a certain probability washingmachine is not used during this day
    washingmachine_usage_prob = float(config['usage_probabilities']['washingmachine_usage_prob'])
    x = np.random.uniform()
    if x > washingmachine_usage_prob:
        return data

    # Reading washingmachine model from configuration file
    washingmachine_model = config['models']['washingmachine_model']

    # Reading the number of possible pattern for the specified model
    washingmachine_patterns = int(config['patterns_for_models']['washingmachine' + str(washingmachine_model)])

    # Select a random pattern between those available and building the corresponding series
    x = np.random.randint(1, washingmachine_patterns + 1)
    filename = 'data/washingmachine/washingmachine_house' + str(washingmachine_model) + "_" + str(x) + ".CSV"
    series = pd.read_csv(filename, header=None, usecols=[1])[1]

    # Altering series
    washingmachine_factor = float(config['alterations']['washingmachine_factor'])
    washingmachine_noise_factor = float(config['alterations']['washingmachine_noise_factor'])
    for i in range(len(series)):
        series[i] = series[i] * np.random.uniform(washingmachine_factor - washingmachine_noise_factor,
                                                  washingmachine_factor + washingmachine_noise_factor)

    # Choosing a start instant
    washingmachine_start = int(config['usage_start']['washingmachine_start'])
    washingmachine_end = int(config['usage_start']['washingmachine_end'])
    mu = np.random.randint(washingmachine_start, washingmachine_end)
    sigma = int(config['usage_start']['washingmachine_sigma'])
    activation_instant = int(np.random.normal(mu, sigma))

    # Building washingmachine data
    for i in range(len(series)):
        data[activation_instant + i] = series[i]

    return data


def microwave(seconds_tenths_in_a_day):
    config = configparser.ConfigParser()
    config.read('resources/config.ini')
    data = np.zeros(seconds_tenths_in_a_day, dtype=None)

    # With a certain probability microwave is not used during this day
    microwave_usage_prob = float(config['usage_probabilities']['microwave_usage_prob'])
    x = np.random.uniform()
    if x > microwave_usage_prob:
        return data

    # Reading microwave model from configuration file
    microwave_model = config['models']['microwave_model']

    # Reading the number of possible pattern for the specified model
    microwave_patterns = int(config['patterns_for_models']['microwave' + str(microwave_model)])

    # Select a random pattern between those available and building the corresponding series
    x = np.random.randint(1, microwave_patterns + 1)
    filename = 'data/microwave/microwave_house' + str(microwave_model) + "_" + str(x) + ".CSV"
    series = pd.read_csv(filename, header=None, usecols=[1])[1]

    # Altering series
    microwave_factor = float(config['alterations']['microwave_factor'])
    microwave_noise_factor = float(config['alterations']['microwave_noise_factor'])
    for i in range(len(series)):
        series[i] = series[i] * np.random.uniform(microwave_factor - microwave_noise_factor,
                                                  microwave_factor + microwave_noise_factor)

    # Choosing a duration for the usage of the appliance and expand the original pattern
    usage_duration = np.random.randint(int(config['usage_duration']['microwave_min']),
                                       int(config['usage_duration']['microwave_max']))
    series = interpolate(usage_duration, len(series), series)

    # Choosing a start instant
    microwave_start = int(config['usage_start']['microwave_start'])
    microwave_end = int(config['usage_start']['microwave_end'])
    mu = np.random.randint(microwave_start, microwave_end)
    sigma = int(config['usage_start']['microwave_sigma'])
    activation_instant = int(np.random.normal(mu, sigma))

    # Building microwave data
    for i in range(len(series)):
        data[activation_instant + i] = series[i]

    return data
