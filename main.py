import ast
import configparser
import os
from periodical_appliances import *
from multi_appliances import *
from datetime import datetime


SECOND_TENTHS_IN_A_DAY: int = 864000
APPLIANCE_TYPE = {
    # PERIODICAL APPLIANCES
    "fridge": "periodical",
    # MULTI PATTERN APPLIANCES
    "dishwasher": "multi",
    "washingmachine": "multi",
    "microwave": "multi",
    "heater": "multi",
}


def generate_appliance_series(appliance):
    sampling_interval = int(config['general']['sampling_interval_seconds'])
    simulation_days = int(config['general']['simulation_days'])

    np_series = np.array([])

    for i in range(simulation_days):
        if APPLIANCE_TYPE[appliance] == "multi":
            np_series = np.concatenate([np_series, multi_appliance_build_data(appliance, config)])
        elif APPLIANCE_TYPE[appliance] == "periodical":
            np_series = np.concatenate([np_series, periodical_appliance_build_data(appliance, config)])

    series = pd.Series(np_series)

    timestamps = pd.date_range(datetime.today().strftime('%Y-%m-%d'),
                               periods=simulation_days * SECOND_TENTHS_IN_A_DAY,
                               freq='0.1S').tz_localize(tz=None)
    series.index = timestamps

    return series.resample('{}S'.format(sampling_interval)).mean()


def generate_dataset():
    sampling_interval = int(config['general']['sampling_interval_seconds'])
    simulation_days = int(config['general']['simulation_days'])

    timestamps = pd.date_range(datetime.today().strftime('%Y-%m-%d'),
                               periods=simulation_days * SECOND_TENTHS_IN_A_DAY / 10 * sampling_interval,
                               freq='{}S'.format(str(sampling_interval))).tz_localize(tz=None)
    aggregate_series = pd.Series(0.0, index=timestamps)

    for appliance in ast.literal_eval(config['model']['appliances']):
        appliance_series = generate_appliance_series(appliance)
        appliance_series.to_csv('target/{}/{}.csv'.format(config['model']['house_ID'], appliance), header=False)

        aggregate_series += appliance_series

    aggregate_series.to_csv('target/{}/{}.csv'.format(config['model']['house_ID'], "aggregate"), header=False)
    return


def set_params(config_file):
    params = configparser.ConfigParser()
    params.read('resources/params')
    for category in params.sections():
        for item in params[category].keys():
            print(params[category][item])
            config_file.set(category, item, params[category][item])


if __name__ == '__main__':
    # Load config file and setting random generator seed
    config = configparser.ConfigParser()
    config.read('resources/config.ini')
    set_params(config)

    np.random.seed(int(config['general']['seed']))

    # Prepare output folder
    try:
        os.mkdir('target/{}'.format(config['model']['house_ID']))
    except FileExistsError:
        pass

    # Generate dataset
    generate_dataset()

    exit()
