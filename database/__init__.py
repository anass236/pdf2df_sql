from config.config import (
    SQLALCHEMY_DATABASE_URI
)
from features import init_feature
from .database import Database
from .read import load_pickle_data


def init_script(w_path):
    stock_df, name_pkl = init_feature(w_path)
    print("--Initialisation of DataBase--\n")
    db = Database(SQLALCHEMY_DATABASE_URI)
    print("--Initialisation OK--\n")
    print("--Inserting of New Data from PDFs--\n")
    upload_result = db.upload_dataframe_to_sql(stock_df, 'monthly_stock')
    print("--Inserting SUCCESSED--\n")
    file_path = w_path + "\\data\\features\\" + name_pkl
    download_result = load_pickle_data(file_path)
    return upload_result, download_result.info()
