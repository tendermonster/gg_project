import numpy as np
import pandas as pd


def initial_playermatrix(grid):
    series = create_series()
    for player in grid.players:
        for i in series:
            if i == "p" or i == "c":
                series[i] = np.append(series[i], getattr(player, f"keep_{i}"))
            elif i == "strategy":
                series[i] = np.append(series[i], getattr(player, i).choice)
            else:
                series[i] = np.append(series[i], getattr(player, i))
    return series

def create_series():  # create series object
    variables = ["id", "c", "p", "b", "money", "strategy",
                "sold_micro", "bought_micro", "sold_main", "bought_main"]
    series = {i:np.array([]) for i in variables}
    return series

def register_stepseries(player):
    series = create_series()
    for i in series:
        if i == "p" or i == "c":
            series[i] = np.append(series[i], getattr(player, f"keep_{i}"))
        elif i == "strategy":
            series[i] = np.append(series[i], getattr(player, i).choice)
        else:
            series[i] = np.append(series[i], getattr(player, i))
    return series


def series_append(total_series, step_series):
    for i in total_series:
        total_series[i] = np.vstack([total_series[i], step_series[i]])
    return total_series
