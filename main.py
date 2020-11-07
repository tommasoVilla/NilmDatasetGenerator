import json
import os
from periodical_appliances import *
from multi_appliances import *
from datetime import datetime

global settings
SECOND_TENTHS_IN_A_DAY: int = 864000
APPLIANCE_MAPPER = {
    # PERIODICAL APPLIANCES
    "fridge": (lambda x: fridge(x)),
    # MULTI PATTERN APPLIANCES
    "dishwasher": (lambda x: dishwasher(x)),
    "washingmachine": (lambda x: washingmachine(x)),
    "microwave": (lambda x: microwave(x)),
}

#prova
def generate_appliance_series(appliance):
    np_series = np.array([])

    for i in range(settings['simulation_days']):
        np_series = np.concatenate([np_series, APPLIANCE_MAPPER[appliance](SECOND_TENTHS_IN_A_DAY)])

    series = pd.Series(np_series)

    timestamps = pd.date_range(datetime.today().strftime('%Y-%m-%d'),
                               periods=settings['simulation_days'] * SECOND_TENTHS_IN_A_DAY,
                               freq='0.1S').tz_localize(tz=None)
    series.index = timestamps

    return series.resample('{}S'.format(settings['sampling_interval_seconds'])).mean()


def generate_dataset():
    sampling_interval = int(settings['sampling_interval_seconds'])
    timestamps = pd.date_range(datetime.today().strftime('%Y-%m-%d'),
                               periods=settings['simulation_days'] * SECOND_TENTHS_IN_A_DAY / 10 * sampling_interval,
                               freq='{}S'.format(str(sampling_interval))).tz_localize(tz=None)
    aggregate_series = pd.Series(0.0, index=timestamps)
    for appliance in settings['appliances']:
        appliance_series = generate_appliance_series(appliance)
        appliance_series.to_csv('target/{}/{}.csv'.format(settings['house_ID'], appliance), header=False)

        aggregate_series += appliance_series

    aggregate_series.to_csv('target/{}/{}.csv'.format(settings['house_ID'], "aggregate"), header=False)
    return


if __name__ == '__main__':

    # Load settings file and setting random generator seed
    settings = json.load(open('resources/settings.json'))
    np.random.seed(settings['seed'])

    # Prepare output folder
    try:
        os.mkdir('target/{}'.format(settings['house_ID']))
    except FileExistsError:
        pass

    # Generate dataset
    generate_dataset()

    exit()
