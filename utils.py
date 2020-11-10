import numpy as np

def interpolate(final_length, current_length, current_data):
    """
    Expand current_data until reach final_length thought interpolation of missing value
    """
    if final_length <= current_length:
        # TODO gestire questo caso
        return current_data

    final_data = np.zeros(final_length, dtype=None)
    up_factor = final_length // current_length
    for i in range(current_length - 1):
        increment = (current_data[i + 1] - current_data[i]) / up_factor
        for j in range(up_factor - 1):
            final_data[((i - 1) * up_factor) + j] = current_data[i] + j * increment
    return final_data
