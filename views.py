import numpy as np
import pandas as pd


def initial_playermatrix(grid):
    series = create_series()
    for player in grid.players:
        series["id"] = np.append(series["id"], player.id)
        series["c"] = np.append(series["c"], player.c)
        series["p"] = np.append(series["p"], player.p)
        series["b"] = np.append(series["b"], player.b)
        series["strategy"] = np.append(series["strategy"], player.strategy.choice)
        series["money"] = np.append(series["money"], player.money)
    return pd.DataFrame.from_dict(
        {
            "id": series["id"],
            "c": series["c"],
            "p": series["p"],
            "b": series["b"],
            "s": series["strategy"],
            "money": series["money"],
        }
    )


def create_series():  # create series object
    id_player, c_player, p_player = np.array([]), np.array([]), np.array([])
    b_player, money_player = np.array([]), np.array([])
    s_player = np.array([])
    series = {
        "id": id_player,
        "c": c_player,
        "p": p_player,
        "b": b_player,
        "money": money_player,
        "strategy": s_player,
    }
    return series


def register_stepseries(grid):
    series = create_series()
    for player in grid.players:
        series["id"] = np.append(series["id"], player.id)
        series["c"] = np.append(series["c"], player.c)
        series["p"] = np.append(series["p"], player.p)
        series["b"] = np.append(series["b"], player.b)
        series["money"] = np.append(series["money"], player.money)
    return series


def series_append(total_series, step_series):
    for i in total_series:
        total_series[i] = np.vstack([total_series[i], step_series[i]])
    return total_series
