import pandas as pd
import numpy as np


# Utility function
# returns moving average given a dataframe and a list of columns and rolling window
def calc_moving_avg(df, col_list, grouping_var, rolling_window):
    df2 = (
        df.groupby(grouping_var)[col_list]
        .rolling(window=rolling_window)
        .mean()
        .reset_index(drop=True)
    )
    return df2


# calculates the rolling sum
def calc_rolling_sum(df, col_list, grouping_var, rolling_window):
    df2 = (
        df.groupby(grouping_var)[col_list]
        .rolling(window=rolling_window)
        .sum()
        .reset_index(0, drop=True)
    )
    return df2


def calc_log(df, col_list):
    # new_col_list = ["log_" + item for item in col_list]
    return df[col_list].apply(lambda x: np.log(x + 1))


def calc_lag(df, col_list, grouping_var, shift_size):
    return df.groupby(grouping_var)[col_list].shift(shift_size)


def find_column_names(column_options, phrase_list):
    return [col for col in column_options for phrase in phrase_list if phrase in col]


def modify_column_names(column_options, modifier, suffix=True):
    if suffix == True:
        return [col + str(modifier) for col in column_options]
    else:
        return [str(modifier) + col for col in column_options]


# https://stackoverflow.com/questions/55475035/tight-layout-cannot-make-axes-height-small-enough-to-accommodate-all-axes-decora
# https://stackoverflow.com/questions/55475035/tight-layout-cannot-make-axes-height-small-enough-to-accommodate-all-axes-decora
# https://stackoverflow.com/questions/29975835/how-to-create-pandas-groupby-plot-with-subplots
# https://stackoverflow.com/questions/60815052/plotting-with-multiple-y-values-with-subplot-and-groupby
