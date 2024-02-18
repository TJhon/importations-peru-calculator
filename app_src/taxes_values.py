import sqlite3
import pandas as pd, os

from app_src.utils import clean_hs

default_taxes = {
    "v_ad_valorem": 4.0,
    "v_igv": 16.0,
    "v_ipm": 2.0,
    "v_antidupping": 0.0,
    "v_insurage": 2.0,
    "default": True,
    "hs_code": "some",
}


def hs_taxes(hscode: str, table_name="taxes_default"):
    hs = clean_hs(hscode)
    default_taxes["hs_code"] = hs

    data_name = "data/base.sqlite"
    # print(os.path.exists(data_name))
    conn = sqlite3.connect(data_name)
    query = f"SELECT * FROM {table_name} WHERE hs_code == {hs}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    search = df.set_index("hs_code").T.to_dict()
    search["hs_code"] = hs

    return search.get(int(hs), default_taxes)


# a = hs_taxes("2933.11.10.100")
# print(a)
