import configparser
import numpy as np
import pandas as pd


def dishwasher(seconds_tenths_in_a_day):
    config = configparser.ConfigParser()
    config.read('resources/config.ini')
    data = np.zeros(seconds_tenths_in_a_day, dtype=None)

    # With a certain probability dishwasher is not used during this day
    dishwasher_usage_prob = float(config['usage_probabilities']['dishwasher_usage_prob'])
    x = np.random.randint(1, 1 / (1 - dishwasher_usage_prob))
    if x == 1:
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
