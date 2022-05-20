import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer
from HM import hungarian_method


def analysis(matrix_lst, sort):
    weights = []
    pairings = []
    time = []
    weights_dict = {}
    time_dict = {}

    N = len(matrix_lst)
    for matrix in matrix_lst:
        start = timer()
        (w, p) = hungarian_method(matrix, sort)
        end = timer()
        time.append(round(end - start, 6))
        weights.append(w)
        pairings.append(p)

    time_dict['average time'] = round(sum(time)/N,6)
    time_dict['max time'] = max(time)
    time_dict['min time'] = min(time)

    weights_dict['average weight'] = round(sum(weights)/N,6)
    weights_dict['max weight'] = max(weights)
    weights_dict['min weight'] = min(weights)

    # if plot_switch == 1:
        # hx, hy, _ = plt.hist(weights, bins=50, normed=1, color="lightblue")
        # plt.ylim(0.0, max(hx)+0.05)
        # plt.title('Weights distribution')
        # plt.grid()
        # plt.show()

    return weights_dict, time_dict

# if __name__ == '__statistics__':
    # analysis()
