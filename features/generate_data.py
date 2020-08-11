import fnmatch
import multiprocessing as mp
import os
import warnings
from multiprocessing import Pool

import pandas as pd
import tabula

warnings.filterwarnings('ignore')


def pdf2df(file_path):
    try:
        columns = [9.5, 28.3, 33.3, 38.4, 42.4, 46.3, 50.3, 54.2, 58.2, 62.1, 66.1, 70, 74, 78, 82, 86, 92, 98.3]
        columns_name = ['CodeRef', 'Name', 'Stock', 'Rotation', 'September', 'October', 'November',
                        'December', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
                        'August', 'Total', 'Last Sale']
        columns_mm = [element * 814.7 / 100 for element in columns]
        df = tabula.read_pdf(file_path, pages='all', guess=False, columns=columns_mm, area=(15, 0, 700, 814.7))
        df = pd.concat(df)
        df.drop(df.index[-1], inplace=True)
        df.reindex()
        df.columns = columns_name
        df.set_index(columns_name[0], inplace=True)
        df.fillna(0, inplace=True)
        os.rename(file_path, file_path[:-4] + '-saved.pdf')
        return df
    except FileNotFoundError:
        return f"File: {file_path} doesn't exist"


def list_pdf2df_parallel(w_path) -> pd.DataFrame:
    print("--Generate Unsaved pdf raws files--\n")
    list_files = [w_path+'\\data\\raws\\'+file for file in os.listdir(w_path+'\\data\\raws')
                  if not fnmatch.fnmatch(file, "*-saved.pdf") and file.endswith(".pdf")]
    pool = Pool(mp.cpu_count())
    df = pd.concat(pool.map(pdf2df, list_files))
    pool.close()
    return df
