from datetime import datetime

from .generate_data import list_pdf2df_parallel
from .process_files import reduce_mem_usage


def init_feature(w_path):
    name_pkl = 'df-Ver.' + datetime.now().strftime('%Y-%m-%d')+'.pkl'
    df = reduce_mem_usage(list_pdf2df_parallel(w_path), name_pkl=name_pkl, w_path=w_path)
    return df, name_pkl
