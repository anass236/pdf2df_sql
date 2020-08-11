import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Float, String, DateTime


class Database:
    """Pandas database client."""

    def __init__(self, db_uri):
        self.engine = create_engine(
            db_uri,
            echo=True
        )

    def dtypes_to_sqltype(self, dtypes) -> dict:
        dictl = {}
        for index, value in dtypes.iteritems():
            if value == np.dtype('float16'):
                dictl[index] = Float
            elif value == np.dtype('int16'):
                dictl[index] = Integer
            elif value == np.dtype('<M8[ns]'):
                dictl[index] = DateTime
            else:
                dictl[index] = String(200)
        return dictl

    def upload_dataframe_to_sql(self, df, table_name):
        """Upload database to database with proper dtypes."""
        df.to_sql(
            table_name,
            self.engine,
            if_exists='append',
            index=False,
            chunksize=500,
            dtype=self.dtypes_to_sqltype(df.dtypes)
        )
        result = f'Loaded {len(df)} rows INTO {table_name} table.'
        print(result)
        return result

    def get_dataframe_from_sql(self, table_name):
        """Create DataFrame form SQL table."""
        table_df = pd.read_sql_table(
            table_name,
            con=self.engine
        )
        result = f'Loaded {len(table_df)} rows FROM {table_name}.'
        print(table_df.info())
        return result
