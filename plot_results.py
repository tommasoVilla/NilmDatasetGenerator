import ast
import configparser

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('resources/config.ini')

    directory_path = 'target/{}/'.format(config['models']['house_ID'])

    main_series = pd.read_csv(directory_path + "aggregate" + ".csv", header=None, usecols=[1])[1]
    plt.figure(figsize=(20, 5))
    plt.title('main')
    plt.plot(np.arange(len(main_series)), main_series, color='blue')
    plt.show()

    for appliance in ast.literal_eval(config['models']['appliances']):
        series = pd.read_csv(directory_path + appliance + ".csv", header=None, usecols=[1])[1]
        plt.figure(figsize=(20, 5))
        plt.title(appliance)
        plt.plot(np.arange(len(series)), series, color='blue')
        plt.show()