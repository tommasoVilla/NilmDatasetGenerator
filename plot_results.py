import ast
import configparser

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import main

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('resources/config.ini')
    main.set_params(config)

    directory_path = 'target/{}/'.format(config['model']['house_ID'])

    main_series = pd.read_csv(directory_path + "aggregate" + ".csv", header=None, usecols=[1])[1]
    plt.figure(figsize=(20, 5))
    plt.title('main')
    plt.plot(np.arange(len(main_series)), main_series, color='blue')
    plt.show()

    for appliance in ast.literal_eval(config['model']['appliances']):
        series = pd.read_csv(directory_path + appliance + ".csv", header=None, usecols=[1])[1]
        plt.figure(figsize=(20, 5))
        plt.title(appliance)
        plt.plot(np.arange(len(series)), series, color='blue')
        plt.show()
