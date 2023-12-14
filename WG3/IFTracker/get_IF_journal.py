import sys
import pandas as pd
import numpy as np
import multiprocessing as mp
from multiprocessing import Pool
from impact_factor.core import Factor

IMPUT_CSV = sys.argv[1]

def add_features(df):
    df[["impact_factor", "predicted_journal", "quartile"]] = df.apply(lambda row: pd.Series(get_impact_factor(row["journal_title"])), axis=1)
    return df

def parallelize_dataframe(df, func, n_cores=mp.cpu_count()):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

def get_impact_factor(journal_name):
    " adds IF of journal to the provided journal title"
    IF = Factor()
    journal_name = str(journal_name).strip()
    if_dict = IF.search(journal_name)

    if if_dict is not None:
        try:
            impact = if_dict[0]["factor"]
            journal_full_name = if_dict[0]["journal"]
            quartile = if_dict[0]["jcr"]
        except:
            impact = np.NaN
            journal_full_name = np.NaN
            quartile = np.NaN

        return pd.Series({"impact_factor": impact, "predicted_journal": journal_full_name, "quartile": quartile})
    else:
        return pd.Series({"impact_factor": np.NaN, "predicted_journal": np.NaN, "quartile": np.NaN})

def add_IF(input_csv):
    print("adding impact factor...")
    sentences_df = pd.read_csv(input_csv, sep="\t")
    tmp_df = sentences_df.copy()
    tmp_parallel_df = parallelize_dataframe(tmp_df, add_features)
    tmp_parallel_df.to_csv(f"./IF_total_journals_def.csv", sep='\t', encoding='utf-8', index=False)

if __name__ == "__main__":
    add_IF(IMPUT_CSV)
