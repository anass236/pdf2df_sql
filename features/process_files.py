# General imports
import os
import warnings

import numpy as np
import pandas as pd
import psutil

# custom imports

warnings.filterwarnings('ignore')


# Simple "Memory profilers" to see memory usage
def get_memory_usage():
    return np.round(psutil.Process(os.getpid()).memory_info()[0] / 2. ** 30, 2)


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


'''
 Memory Reducer
    :df pandas dataframe to reduce size             # type: pd.DataFrame()
    :verbose                                        # type: bool
'''


def reduce_mem_usage(df, name_pkl, w_path, verbose=True):
    print("--Reduce memory--\n")
    columns_name = df.columns
    for name in columns_name[1:-1]:
        if df[name].dtype == object:
            df[name] = pd.to_numeric(df[name], errors='coerce')
    # "Last Sale" Column
    df.iloc[:, -1] = pd.to_datetime(df.iloc[:, -1], errors='coerce')
    df.index = pd.to_numeric(df.index, errors='coerce')
    df.fillna(0, inplace=True)

    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024 ** 2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    end_mem = df.memory_usage().sum() / 1024 ** 2
    if verbose:
        print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem,
                                                                              100 * (start_mem - end_mem) / start_mem))
    path_pkl = w_path + '\\data\\features\\' + name_pkl
    df.to_pickle(path_pkl)
    return df
